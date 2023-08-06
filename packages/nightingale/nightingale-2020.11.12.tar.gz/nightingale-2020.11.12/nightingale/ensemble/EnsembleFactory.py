from sklearn.linear_model import LinearRegression
from pandas import DataFrame
from pensieve import Pensieve


class Layer:
	def __init__(self, models, name_numbers=None, pensieve=None, interaction=True):
		"""
		:type models: dict[str, LinearRegression] or list[LinearRegression]
		:type name_numbers: dict[str, int] or NoneType
		:type pensieve: Pensieve or NoneType
		"""
		if name_numbers is None:
			name_numbers = {}
		if isinstance(models, (list, tuple)):
			models_dictionary = {}
			for model in models:
				name = type(model).__name__
				if name not in name_numbers:
					name_numbers[name] = 1
				else:
					name_numbers[name] += 1
				models_dictionary[f'{name}_{name_numbers[name]}'] = model
			models = models_dictionary

		self._models = models
		self._interaction = interaction
		self._pensieve = pensieve

	@property
	def models(self):
		"""
		:rtype: dict[str, LinearRegression]
		"""
		return self._models

	@property
	def pensieve(self):
		"""
		:rtype: Pensieve or NoneType
		"""
		return self._pensieve

	def fit(self, X, y):
		for model_name, model in self.models.items():
			model.fit(X=X, y=y)
			if self.pensieve is not None:
				self.pensieve[model_name] = model

	@staticmethod
	def _predict_with_models(models_dictionary, X, interaction, last_layer=False):

		def predict_or_transform(model, X):
			try:
				return model.predict(X=X)
			except AttributeError:
				return DataFrame(model.transform(X=X))

		if len(models_dictionary) > 1 or not last_layer:
			data_dictionary = {}
			for model_name, model in models_dictionary.items():
				prediction = predict_or_transform(model=model, X=X)
				if isinstance(prediction, DataFrame):
					for column_num, column in enumerate(prediction.columns):
						data_dictionary[f'{model_name}_prediction_{column_num + 1}'] = prediction[column]
				else:
					data_dictionary[f'{model_name}_prediction'] = prediction

			if interaction:
				new_dictionary = {}
				for key1, value1 in data_dictionary.items():
					for key2, value2 in data_dictionary.items():
						new_dictionary[f'{key1}__{key2}'] = value1 * value2
			data_dictionary.update(new_dictionary)
			return DataFrame(data_dictionary)

		else:
			return models_dictionary[list(models_dictionary.keys())[0]].predict(X=X)

	def predict(self, X, x_name='X', y_name='y', materialize=True, last_layer=False):
		if self.pensieve is not None:
			if X is not None:
				self.pensieve[x_name] = X

			def create_predict_function(models, x_name, last_layer):
				def predict_function(x):
					return self._predict_with_models(
						models_dictionary={model_name: x[model_name] for model_name, model in models.items()},
						X=x[x_name],
						last_layer=last_layer, interaction=self._interaction
					)
				return predict_function
			self.pensieve.store(
				key=y_name, precursors=[x_name] + list(self.models.keys()),
				function=create_predict_function(models=self.models, x_name=x_name, last_layer=last_layer),
				materialize=materialize
			)
			return self.pensieve[y_name]

		else:
			return self._predict_with_models(
				models_dictionary=self.models, X=X, last_layer=last_layer, interaction=self._interaction
			)


class Ensemble:
	def __init__(self, layers, pensieve=None, interaction=True):
		"""
		:type layers: list[dict[str, LinearRegression]] or list[list[LinearRegression]]
		:type pensieve: Pensieve or NoneType
		"""
		name_numbers = {}
		self._layers = []
		self._pensieve = pensieve
		self._interaction = interaction
		for models in layers:
			self._layers.append(
				Layer(models=models, name_numbers=name_numbers, pensieve=self.pensieve, interaction=self._interaction)
			)

	@property
	def layers(self):
		"""
		:type: list[Layer]
		"""
		return self._layers

	@property
	def output_model(self):
		"""
		:rtype: LinearRegression
		"""
		return self._output_model

	@property
	def pensieve(self):
		"""
		:rtype: Pensieve or NoneType
		"""
		return self._pensieve

	def fit(self, X, y):
		for layer in self.layers:
			layer.fit(X=X, y=y)
			X = layer.predict(X=X, last_layer=False)
			#print(X.shape)

	def predict(self, X):
		for layer_number, layer in enumerate(self.layers):
			if layer_number == 0:
				x_name = 'X'
			else:
				x_name = f'X_{layer_number + 1}'

			if layer_number + 1 == len(self.layers):
				y_name = 'y'
			else:
				y_name = f'X_{layer_number + 2}'

			X = layer.predict(
				X=X if layer_number==0 or self.pensieve is None else None,
				x_name=x_name, y_name=y_name, last_layer=layer_number + 1 == len(self.layers)
			)
			#print(X.shape)

		return X
