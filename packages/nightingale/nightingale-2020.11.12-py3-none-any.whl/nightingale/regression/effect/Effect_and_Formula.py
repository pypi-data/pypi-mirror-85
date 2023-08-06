from .MainEffect import MainEffect
from .InteractionEffect import InteractionEffect


def Effect(formula, p=None, coefficient=None):
	"""
	:type formula: str
	:rtype: InteractionEffect or MainEffect
	"""
	if ':' in formula or '*' in formula:
		return InteractionEffect(formula=formula, p=p, coefficient=coefficient)
	else:
		return MainEffect(formula=formula, p=p, coefficient=coefficient)


###############################################################################


class Formula:
	def __init__(self, formula):
		"""
		:type formula: Formula or str
		"""
		if isinstance(formula, Formula):
			self._xs = formula._xs
			self._y = formula._y
		else:
			if '~' in formula:
				y, xs = formula.split('~')
				y, xs = y.strip(), xs.strip()
				self._y = MainEffect(formula=y)
			else:
				xs = formula
				self._y = None
			self._xs = sorted([Effect(formula=x) for x in xs.split('+')], key=lambda x: (x.num_interactions, x.name))

	@classmethod
	def from_variables(cls, independent_variables, dependent_variable=None):
		"""
		:type dependent_variable: NoneType or MainEffect
		:type independent_variables: list[MainEffect or InteractionEffect]
		:rtype: Formula
		"""
		x_formula = ' + '.join([x.formula for x in independent_variables])
		if dependent_variable is None:
			return cls(formula=x_formula)
		else:
			return cls(formula=f'{dependent_variable.formula} ~ {x_formula}')

	def represent(self, multiply_symbol='×'):
		x_formula = ' + '.join([x.represent(multiply_symbol=multiply_symbol) for x in self.effects])
		if self.dependent_variable is None:
			return x_formula
		else:
			return f'{self.dependent_variable.formula} ~ {x_formula}'

	@property
	def formula(self):
		return self.represent(multiply_symbol='*')

	def __str__(self):
		return self.represent(multiply_symbol='×')

	def __repr__(self):
		return self.__str__()

	def display(self):
		x_formula = ' + \n'.join(['\t' + x.formula for x in self.effects])
		if self.dependent_variable is None:
			return x_formula
		else:
			return f'{self.dependent_variable.formula} ~ \n{x_formula}'

	@property
	def dependent_variable(self):
		"""
		:rtype: MainEffect
		"""
		return self._y

	@property
	def effects(self):
		"""
		:rtype: list[InteractionEffect or MainEffect]
		"""
		return self._xs

	@property
	def independent_variables(self):
		"""
		:rtype: list[MainEffect]
		"""
		result = []
		for x in self._xs:
			if isinstance(x, MainEffect):
				if x not in result:
					result.append(x)
			elif isinstance(x, InteractionEffect):
				for z in x.main_effects:
					if z not in result:
						result.append(z)
		return result
