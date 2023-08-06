from pandas import DataFrame, concat
from numpy import nan, isnan
from statsmodels.api import OLS, GEE, Logit
from statsmodels.api import families
from ravenclaw.wrangling import bring_to_front
from chronometry.progress import ProgressBar
import re

from .effect import Formula, MainEffect, InteractionEffect, Effect
from .convert_simple_table_to_dataframe import convert_simple_table_to_dataframe
from .convert_camel_to_snake import convert_camel_to_snake
from .exceptions import BrokenModel, BrokenSummary, FormulaError


class Regression:
	def __init__(
			self, data, model_builder, formula, significance_level=0.05, family=None, groups=None, parent=None
	):
		"""
		:type data: DataFrame
		:type model_builder: callable
		:type formula: str or Formula
		:type significance_level: float
		:type family: families.Binomial or families.Family or NoneType
		:type groups: NoneType or str or list[str]
		:type previous_formulas: NoneType or list[Formula]
		"""
		self._formula = Formula(formula)
		if self._formula.dependent_variable is None:
			raise FormulaError(f'dependent variable missing from {self._formula}!')
		self._groups = groups
		self._data = data
		self._significance_level = significance_level
		self._model_builder = model_builder
		self._family = family
		self._groups = groups

		self._variables = {effect.name: effect for effect in self._formula.effects}
		self._model = None
		self._fit = None
		self._summary = None
		self._summary_table = None
		self._parent = parent
		self._effects = None
		self._significant_interaction_effects = None
		self._significant_main_effects = None
		self._insignificant_interaction_effects = None
		self._insignificant_main_effects = None

	def __repr__(self):
		return f'formula: {self.formula.represent()}\ngroups: {self.groups}\nfamily: {self.family}'

	def __str__(self):
		return self.__repr__()

	@property
	def formulas(self):
		"""
		:rtype: list[Formula]
		"""
		if self._parent is None:
			return [self.formula]
		else:
			return self._parent.formulas + [self.formula]

	def display(self, p=None):
		try:
			from IPython.core.display import display
			display((
				self._model_builder,
				{
					'formula': self.formula,
					'groups': self.groups,
					'family': self.family,
					'summary_table': self._summary_table
				},
				self.data.head()
			))
		except ImportError:
			if p is not None:
				p.pretty(self.__repr__())
			else:
				print(self.__repr__())

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text('Regression')
		else:
			self.display(p=p)

	def build_model(self):
		"""
		:rtype: OLS or GEE or Logit
		"""
		if self.family is None and self.groups is None:
			model = self._model_builder(formula=self.formula.formula, data=self.data)
		elif self.family is None:
			model = self._model_builder(formula=self.formula.formula, data=self.data, groups=self.groups)
		elif self.groups is None:
			model = self._model_builder(formula=self.formula.formula, data=self.data, family=self.family)
		else:
			model = self._model_builder(
				formula=self.formula.formula, data=self.data, groups=self.groups, family=self.family
			)
		return model

	@property
	def variables(self):
		"""
		:rtype: dict[str, MainEffect or InteractionEffect]
		"""
		return self._variables

	@property
	def model(self):
		"""
		:rtype: OLS or GEE or Logit
		"""
		if self._model is None:
			self._model = self.build_model()
		return self._model

	@property
	def fit(self):
		"""
		:rtype: OLS or GEE or Logit
		"""
		if self._fit is None:
			try:
				self._fit = self.model.fit()
			except Exception as e:
				self._fit = BrokenModel(exception=e, regression=self)

		return self._fit

	@property
	def parameters(self):
		"""
		:rtype: dict
		"""
		return dict(self.fit.params)

	@property
	def coef_(self):
		return {key: value for key, value in self.parameters.items() if key.lower() != 'intercept'}

	@property
	def intercept_(self):
		try:
			return self.parameters['Intercept']
		except KeyError:
			return self.parameters['intercept']

	@property
	def feature_importances_(self):
		return self.fit.feature_importances_

	def predict(self, data):
		return self.fit.predict(data)

	@property
	def summary(self):
		if self._summary is None:
			self._summary = self.fit.summary()
		return self._summary

	@property
	def coefficient_table(self):
		"""
		:rtype: DataFrame
		"""
		if isinstance(self.summary, BrokenSummary):
			return DataFrame({'error': [self.summary.model.exception]})
		else:
			return convert_simple_table_to_dataframe(self.summary.tables[1]).rename(columns={
				'coef': 'coefficient', 'std err': 'standard_error', '[0.025': 'lower_0.025',
				'0.975]': 'upper_0.975', 'P>|z|': 'p'
			})

	@property
	def model_table(self):
		"""
		:rtype: DataFrame
		"""
		result = convert_simple_table_to_dataframe(self.summary.tables[2], header=False).reset_index()
		tables = []
		for i in range(result.shape[1]//2):
			table = result.iloc[:, i*2:i*2+2]
			table.columns = ['name', 'value']
			tables.append(table)
		result = concat(tables).reset_index(drop=True)

		def clean_variable_name(x):
			x = x.strip()
			x = re.sub(':\s*$', '', x)
			x = re.sub('-', ' ', x)
			x = re.sub('[^a-zA-Z\d\s:]', ' ', x)
			x = '_'.join(x.split())

			x = convert_camel_to_snake(x)
			x = re.sub('\s+', '', x)
			return x

		result['name'] = result['name'].apply(clean_variable_name)
		return result.set_index(keys='name')

	@property
	def summary_table(self):
		if self._summary_table is None:
			table = self.coefficient_table

			if not isinstance(self.summary, BrokenSummary):
				for column in table.columns:
					if column != 'coefficient':
						table[column] = table[column].astype(float)
				table['variable_formula'] = table.index
				table['p'] = table['p']

				effects = table.apply(
					func=lambda x: Effect(formula=x['variable_formula'], p=x['p'], coefficient=x['coefficient']),
					axis=1
				)
				table['num_interactions'] = effects.apply(func=lambda x: x.num_interactions)

				max_num_interactions = table['num_interactions'].max()

				variables = []

				def get_name(effect):
					if effect is None:
						return None
					else:
						return effect.name

				for i in range(max_num_interactions + 1):
					variable = f'variable_{i+1}'
					table[variable] = effects.apply(func=lambda x: get_name(x.get_variable(i, missing=None)))
					variables.append(variable)

				table['effect'] = effects
				table['effect_type'] = effects.apply(func=lambda x: x.type)
				table['categorical_level'] = effects.apply(func=lambda x: x.categorical_level)
				table['relative'] = effects.apply(func=lambda x: x.relative)

				table['effect_name'] = effects.apply(func=lambda x: x.name)

				table['minimum_variable_p'] = table.groupby(by='effect')['p'].transform('min')

				table['significant'] = table['minimum_variable_p'] < self.significance_level

				# get other levels for all categorical
				base_levels = table[
					(table['effect_type'] == 'categorical') & (table['relative'])
					][['effect', 'categorical_level']].groupby(
					by='effect'
				).apply(lambda x: list(set(self.data[x['effect'][0]]) - set(x['categorical_level']))[0]).reset_index().rename(
					columns={0: 'base_level'}
				)
				table = table.merge(right=base_levels, on='effect', how='left')

				table['is_intercept'] = table['effect'] == 'intercept'
				table.sort_values(by=['is_intercept', 'minimum_variable_p'], ascending=[False, True], inplace=True)
				if 'base_level' not in table.columns:
					table['base_level'] = None
				table = table.replace({nan: None})
				self._summary_table = bring_to_front(
					data=table.drop(
						columns=['minimum_variable_p', 'is_intercept', 'relative']
					).reset_index(drop=True),
					columns=['effect_type', 'effect', 'num_interactions'] + variables + ['categorical_level', 'base_level', 'significant', 'p']
				)
			else:
				self._summary_table = DataFrame({
					column: [None] for column in [
						'effect_type', 'effect', 'num_interactions', 'categorical_level', 'base_level', 'significant', 'p'
					]
				})
				self._summary_table['error'] = self.summary.model.exception

		return self._summary_table

	@property
	def family(self):
		"""
		:rtype: families.Binomial or families.Family or NoneType
		"""
		return self._family

	@property
	def groups(self):
		"""
		:rtype: NoneType or str or list[str]
		"""
		return self._groups

	@property
	def formula(self):
		"""
		:rtype: Formula
		"""
		return self._formula

	@property
	def data(self):
		"""
		:rtype: DataFrame
		"""
		return self._data

	@property
	def significance_level(self):
		"""
		:rtype: float
		"""
		return self._significance_level

	@property
	def except_intercept(self):
		return self.summary_table[self.summary_table['effect_type'] != 'intercept']

	@property
	def num_significant_effects(self):
		try:
			return len(self.except_intercept[self.except_intercept['significant']])
		except TypeError as e:
			if len(self.except_intercept) < 2:
				return None
			else:
				print(self.except_intercept)
				raise e

	@property
	def num_insignificant_effects(self):
		return len(self.insignificant_effects)

	@property
	def effects(self):
		if self._effects is None:
			self._effects = sorted(self.except_intercept['effect'], key=lambda x: x.p)
		return self._effects

	@property
	def significant_interaction_effects(self):
		"""
		:rtype: list[InteractionEffect]
		"""
		if self._significant_interaction_effects is None:
			self._significant_interaction_effects = [
				effect for effect in self.effects
				if isinstance(effect, InteractionEffect) and (effect.p < self._significance_level or isnan(effect.p) or effect.p is None)
			]
		return self._significant_interaction_effects

	@property
	def insignificant_interaction_effects(self):
		"""
		:rtype: list[InteractionEffect]
		"""
		if self._insignificant_interaction_effects is None:
			self._insignificant_interaction_effects = [
				effect for effect in self.effects
				if isinstance(effect, InteractionEffect) and effect.p >= self._significance_level and not isnan(effect.p) and effect.p is not None
			]
		return self._insignificant_interaction_effects

	def is_main_effect_significant(self, main_effect):
		"""
		:type main_effect: MainEffect
		:rtype: bool
		"""
		return any([
			interaction.contains(main_effect) for interaction in self.significant_interaction_effects
		]) or main_effect.p < self.significance_level

	@property
	def significant_main_effects(self):
		"""
		:rtype: list[MainEffect]
		"""
		if self._significant_main_effects is None:
			self._significant_main_effects = [
				effect for effect in self.effects
				if isinstance(effect, MainEffect) and self.is_main_effect_significant(effect)
			]
		return self._significant_main_effects

	@property
	def insignificant_main_effects(self):
		"""
		:rtype: list[MainEffect]
		"""
		if self._insignificant_main_effects is None:
			self._insignificant_main_effects = [
				effect for effect in self.effects
				if isinstance(effect, MainEffect) and not self.is_main_effect_significant(effect)
			]
		return self._insignificant_main_effects

	@property
	def insignificant_effects(self):
		"""
		:rtype: list[MainEffect or InteractionEffect]
		"""
		return self.insignificant_main_effects + self.insignificant_interaction_effects

	@property
	def least_significant_insignificant_effect(self):
		return self.insignificant_effects[-1]

	@property
	def all_effects_but_least_significant(self):
		return [effect for effect in self.effects if effect != self.least_significant_insignificant_effect]

	def eliminate(self, num_rounds=None, echo=1):
		"""
		:type num_rounds: int or NoneType
		:type echo: bool or int
		:rtype: Regression
		"""
		model = self
		if isinstance(model.fit, BrokenModel):
			return self

		num_rounds = num_rounds or len(self.variables)
		progress_bar = ProgressBar(total=num_rounds, echo=echo)
		round = 0
		previous_lse = None
		previous_formula = None
		for round in range(num_rounds):

			if model.num_insignificant_effects < 1:
				break

			else:
				y = model.formula.dependent_variable


				lse = model.least_significant_insignificant_effect
				xs = model.all_effects_but_least_significant
				progress_bar.show(
					amount=round,
					text=f'effects: {len(xs)+1}, eliminating {lse} with p={lse.p}'
				)
				new_formula = Formula.from_variables(
					independent_variables=xs,
					dependent_variable=y
				)

				if previous_lse == lse:
					print('eliminating', lse, '\n\n')
					print('is main effect insignificant?', model.is_main_effect_significant(lse), '\n\n')
					for interaction in model.significant_interaction_effects:
						print(interaction, 'contains?', interaction.contains(lse))

					for interaction in model.insignificant_interaction_effects:
						print(interaction, interaction.p)

					print(model.least_significant_insignificant_effect, lse)
					print('\n\ninsignificant effects\n', model.insignificant_effects)
					print(new_formula.display())

					for x in xs:
						print(x, x.num_interactions, x.p)
					raise RuntimeError(f'repeating the elimination of {lse}')

				previous_formula = new_formula
				previous_lse = lse


				new_model = model.__class__(
					data=model.data, formula=new_formula, significance_level=model.significance_level,
					groups=model.groups, family=model.family, model_builder=model._model_builder,
					parent=model
				)



				if isinstance(new_model.fit, BrokenModel):
					break

				else:
					model = new_model

		progress_bar.show(
			amount=round + 1,
			text=f'effects: {len(model.formula.independent_variables)}'
		)
		return model
