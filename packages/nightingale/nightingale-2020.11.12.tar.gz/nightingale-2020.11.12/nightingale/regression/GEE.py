import statsmodels.formula.api as smf
from statsmodels.api import families
from .Regression import Regression


class BasicGEE(Regression):
	def __init__(self, data, formula, significance_level=0.05, family=None, groups=None, model_builder=None, parent=None):
		super().__init__(
			data=data, formula=formula, model_builder=smf.gee, groups=groups, family=family,
			significance_level=significance_level, parent=parent
		)

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
		return super().coefficient_table.rename(columns={'P>|z|': 'p'})


class GEE(BasicGEE):
	def __init__(self, data, formula, groups=None, significance_level=0.05, model_builder=None, family=None, parent=None):
		super().__init__(
			data=data, formula=formula,  groups=groups, significance_level=significance_level, parent=parent
		)

	@property
	def name(self):
		"""
		:rtype: str
		"""
		return 'gee'

class LogisticGEE(BasicGEE):
	def __init__(self, data, formula, groups=None, significance_level=0.05, model_builder=None, family=None, parent=None):
		super().__init__(
			data=data, formula=formula, groups=groups, family=families.Binomial(),
			significance_level=significance_level, parent=parent
		)

	@property
	def name(self):
		"""
		:rtype: str
		"""
		return 'logistic_gee'
