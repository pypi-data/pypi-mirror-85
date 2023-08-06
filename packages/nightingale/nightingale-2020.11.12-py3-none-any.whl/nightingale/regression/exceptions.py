class RegressionError(Exception):
	pass

class FormulaError(RegressionError):
	pass

class EliminationError(RegressionError):
	pass

class AllValuesSignificantError(EliminationError):
	pass

class NoIndependentVariableError(EliminationError):
	pass


class BrokenSummary:
	def __init__(self, model):
		self._model = model

	@property
	def model(self):
		"""
		:rtype: BrokenModel
		"""
		return self._model


class BrokenModel:
	def __init__(self, exception, regression):
		"""
		:type exception: Exception
		:type regression: Regression
		"""
		self._exception = exception
		self._formula = regression.formula
		self._family = regression.family
		self._groups = regression.groups
		self._model_builder = regression._model_builder

	@property
	def exception(self):
		return self._exception

	def summary(self):
		return BrokenSummary(model=self)