from pandas import DataFrame, Series
from copy import deepcopy


class PredictableData:
	def __init__(self, model, X):
		"""
		:param model:
		:type X: DataFrame
		"""
		self._model = model
		self._model_is_fitted = False
		self._X = X

	def fit(self, y=None, **kwargs):
		"""
		:type y: Series or list
		:type kwargs: dict
		:rtype: PredictableData
		"""
		if y is None:
			self._model.fit(self._X, **kwargs)
		else:
			self._model.fit(self._X, y, **kwargs)
		return self

	def predict(self, **kwargs):
		"""
		:type kwargs: dict
		:rtype: Series or list
		"""
		if hasattr(self._model, 'predict'):
			return self._model.predict(self._X, **kwargs)
		elif hasattr(self._model, 'pred'):
			return self._model.pred(self._X, **kwargs)
		else:
			raise AttributeError(f'{self._model} does not have any of predict or pred attributes!')

	@property
	def X(self):
		"""
		:rtype: DataFrame
		"""
		return self._X


class Predictor:
	def __init__(self, model, transformer=None, model_is_fitted=False, transformer_is_fitted=False, x_columns=None):
		self._transformer = transformer
		self._transformer_is_fitted = transformer_is_fitted or transformer is None
		self._unfitted_transformer = None
		self._model = model
		self._model_is_fitted = model_is_fitted
		self._unfitted_model = None
		self._x_columns = x_columns

	_STATE_ATTRIBUTES = ['_transformer', '_transformer_is_fitted', '_unfitted_transformer', '_model', '_model_is_fitted', '_unfitted_model', '_x_columns']

	def __getstate__(self):
		return {key: getattr(self, key) for key in self._STATE_ATTRIBUTES}

	def __setstate__(self, state):
		for key, value in state.items():
			setattr(self, key, value)

	@property
	def original_transformer(self):
		return self._unfitted_transformer or self._transformer

	@property
	def original_model(self):
		if self._unfitted_model is None:
			return self._model
		else:
			return self._unfitted_model

	def fit_transformer(self, X, **kwargs):
		"""
		:type X: DataFrame
		:type kwargs: dict
		:rtype: Predictor
		"""
		if self._transformer is not None:
			self._unfitted_transformer = deepcopy(self._transformer)
			self._transformer.fit(X, **kwargs)
		self._transformer_is_fitted = True
		self._x_columns = list(X.columns)
		return self

	def fit_model(self, X, y=None, **kwargs):
		"""
		:type X: DataFrame
		:type y: NoneType or Series or list
		:type kwargs: dict
		:rtype: Predictor
		"""
		self._unfitted_model = deepcopy(self._model)
		self.transform(X=X).fit(y=y, **kwargs)
		self._model_is_fitted = True
		if self._transformer is None:
			self._x_columns = list(X.columns)
		return self

	def fit(self, X, y=None, **kwargs):
		if self._transformer_is_fitted:
			self.fit_model(X=X, y=y, **kwargs)
		else:
			self.fit_transformer(X=X).fit_model(X=X, y=y, **kwargs)

	def transform(self, X, **kwargs):
		"""
		:type X: DataFrame
		:rtype: PredictableData
		"""
		if not self._transformer_is_fitted:
			raise RuntimeError('transformer is not fitted!')
		if self._x_columns:
			X = X[self._x_columns]

		if self._transformer is None:
			transformed = X
		elif hasattr(self._transformer, 'transform'):
			transformed = self._transformer.transform(X, **kwargs)
		elif hasattr(self._transformer, 'predict'):
			transformed = self._transformer.predict(X, **kwargs)
		elif hasattr(self._transformer, 'pred'):
			transformed = self._transformer.pred(X, **kwargs)
		else:
			raise AttributeError(f'{self._transformer} does not have any of transform, predict, or pred attributes!')

		return PredictableData(model=self._model, X=transformed)

	def predict(self, X, **kwargs):
		"""
		:type X: DataFrame
		:rtype: Series or list
		"""
		return self.transform(X=X).predict(**kwargs)
