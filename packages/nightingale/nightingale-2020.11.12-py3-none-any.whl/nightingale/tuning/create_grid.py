from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.base import MultiOutputMixin
from sklearn.base import RegressorMixin

from slytherin.collections import create_grid


def create_model_grid(model, dictionary, name=None):
	list_of_dictionaries = create_grid(dictionary=dictionary)
	models = {}
	parameters_list = []
	parameters_dictionary = {}
	for index, kwargs in enumerate(list_of_dictionaries):
		model_name = f'{name}_{index}'
		models[model_name] =  model(**kwargs)
		parameters = kwargs.copy()
		parameters['model'] = model_name
		parameters_list.append(parameters)
		parameters_dictionary[model_name] = kwargs.copy()
	return {'models': models, 'parameter_table': DataFrame.from_records(parameters_list), 'parameters': parameters_dictionary}


class ModelGrid:
	def __init__(self, grid_dictionaries, models=None):
		"""
		:type grid_dictionaries: list[dict] or dict
		:type models: LinearRegression or MultiOutputMixin or RegressorMixin
		"""
		if models is None:
			models = [x['model'] for x in grid_dictionaries]
			for grid_dict in grid_dictionaries:
				del grid_dict['model']

		if not isinstance(models, list):
			models = [models]

		if not isinstance(grid_dictionaries, list):
			grid_dictionaries = [grid_dictionaries]

		num_models_per_type = {}
		out_models = {}
		records = []
		parameter_dictionary = {}
		for model, dictionary in zip(models, grid_dictionaries):
			list_of_dictionaries = create_grid(dictionary=dictionary)

			for index, kwargs in enumerate(list_of_dictionaries):
				try:
					model_type = model.__name__
				except AttributeError:
					model_type = 'model'

				if model_type not in num_models_per_type:
					num_models_per_type[model_type] = 1
				else:
					num_models_per_type[model_type] += 1

				model_name = f'{model_type}_{num_models_per_type[model_type]}'
				out_models[model_name] = model(**kwargs)
				parameters = kwargs.copy()
				parameters['model_name'] = model_name
				records.append(parameters)
				parameter_dictionary[model_name] = kwargs.copy()

		self.models = out_models
		self.num_models_per_type = num_models_per_type
		self.parameters = parameter_dictionary
		self.parameter_table = DataFrame.from_records(records)

