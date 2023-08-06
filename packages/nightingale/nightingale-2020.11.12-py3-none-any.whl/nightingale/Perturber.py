from ravenclaw import is_numeric
from pandas import DataFrame
from pensieve import Pensieve


class PerturbedFeature:
	def __init__(
			self, data, output_column, input_column, output_column_type='numeric', transformation_function=None,
			perturbation_ratio=0.01
	):
		self._pensieve = Pensieve(graph_direction='LR')
		self.pensieve['data'] = data
		self.pensieve['perturbation_ratio'] = perturbation_ratio

		self.pensieve.store(
			key='transformed_data',
			function=lambda data: data.copy() if transformation_function is None else transformation_function(data),
			materialize=False,
			evaluate=False
		)

		if output_column_type != 'numeric':
			self.pensieve['output_value_counts'] = lambda transformed_data: dict(
				transformed_data[output_column].value_counts(dropna=False)
			)




	@property
	def pensieve(self):
		"""
		:rtype: Pensieve
		"""
		return self._pensieve

class Perturber:
	def __init__(
			self, data, output_column, output_column_type='numeric', function=None, input_columns=None,
			perturbation_ratio=0.01
	):
		"""
		:param DataFrame data: a data frame that should be perturbed
		:param callable function: a transformation function to be run on data after perturbation
		:param str output_column: the column whose value should be examined for the effect of perturbation
		:param int or float perturbation_ratio: the amount of perturbation as a ratio of the standard deviation of the perturbed column
		"""



		self._input_columns = input_columns or [column for column in data.columns if column != output_column]






		memory_list = []
		for column in self._input_columns:
			memory_dictionary = {'column': column}

			def get_perturbed_data(data, column, perturbation_ratio):
				if is_numeric(data[column]):
					new_data = data.copy()
					new_data[column] = data[column] + perturbation_ratio * data[column].std()
					return transformation_function(new_data)
				else:
					result = {}
					for category in set(data[column].values):
						new_data = data.copy()
						new_data[column] = category
						result[category] = transformation_function(new_data)
					return result

			perturbed_key = f'transformed_data__{column}_perturbed'

			def create_perturbed_data_function(column):
				def function(x):
					return get_perturbed_data(
						data=x['data'],
						column=column,
						perturbation_ratio=x['perturbation_ratio']
					)
				return function

			self.pensieve.store(
				key=perturbed_key,
				precursors=['data', 'perturbation_ratio'],
				function=create_perturbed_data_function(column=column),
				materialize=False,
				evaluate=False
			)

			if output_column_type == 'numeric':

				def get_mean_difference(perturbed_data, transformed_data):
					if isinstance(perturbed_data, dict):
						result = {}
						for key, data in perturbed_data.items():
							result[key] = data[output_column].mean() - transformed_data[output_column].mean()
						return result
					else:
						return perturbed_data[output_column].mean() - transformed_data[output_column].mean()

				def create_mean_difference_function(perturbed_key):
					def function(x):
						return get_mean_difference(
							perturbed_data=x[perturbed_key],
							transformed_data=x['transformed_data']
						)
					return function

				self.pensieve.store(
					key=f'mean_difference__{column}_perturbed',
					precursors=[perturbed_key, 'transformed_data'],
					function=create_mean_difference_function(perturbed_key=perturbed_key),
					evaluate=False
				)
				memory_dictionary['mean_difference'] = f'mean_difference__{column}_perturbed'

				def get_difference_ratio(mean_difference_column_perturbed, transformed_data, column):
					if isinstance(mean_difference_column_perturbed, dict):
						return None
					else:
						if mean_difference_column_perturbed == 0:
							return 0
						else:
							return mean_difference_column_perturbed / (transformed_data[column].std() * perturbation_ratio)

				def create_mean_difference_ratio(column):
					def function(x):
						return get_difference_ratio(
							mean_difference_column_perturbed=x[f'mean_difference__{column}_perturbed'],
							transformed_data=x['transformed_data'],
							column=column
						)
					return function

				self.pensieve.store(
					key=f'difference_ratio__{column}_perturbed',
					precursors=['transformed_data', f'mean_difference__{column}_perturbed'],
					function=create_mean_difference_ratio(column=column),
					evaluate=False
				)
				memory_dictionary['difference_ratio'] = f'difference_ratio__{column}_perturbed'

			else:

				def get_count_difference(perturbed_data, output_value_counts):
					if isinstance(perturbed_data, dict):
						result = {}
						for category, data in perturbed_data.items():
							perturbed_value_counts = dict(data[output_column].value_counts(dropna=False))
							count_differences = {}
							for result_category in set(output_value_counts.keys()).union(set()):
								count_differences[result_category] = perturbed_value_counts.get(result_category, 0) - \
																	 output_value_counts.get(result_category, 0)
							result[category] = count_differences
					else:
						perturbed_value_counts = dict(perturbed_data[output_column].value_counts(dropna=False))
						count_differences = {}
						for result_category in set(output_value_counts.keys()).union(set()):
							count_differences[result_category] = perturbed_value_counts.get(result_category,0) - \
																 output_value_counts.get(result_category, 0)
						return count_differences

				def create_count_difference_function(perturbed_key):
					def function(x):
						return get_count_difference(
							perturbed_data=x[perturbed_key],
							output_value_counts=x['output_value_counts'],
						)
					return function

				self.pensieve.store(
					key=f'count_difference__{column}_perturbed',
					precursors=[perturbed_key, 'transformed_data', 'output_value_counts'],
					function=create_count_difference_function(perturbed_key=perturbed_key),
					evaluate=False
				)
				memory_dictionary['count_difference'] = f'count_difference__{column}_perturbed'

			memory_list.append(memory_dictionary)

		def create_summary(memory_list):
			def function(x):
				result_list = []
				for memory_dictionary in memory_list:
					result_dictionary = {'column': memory_dictionary['column']}
					for memory_key_key, memory_key in memory_dictionary.items():
						if memory_key_key != 'column':
							result_dictionary[memory_key_key] = x[memory_key]
					result_list.append(result_dictionary)
				return result_list
			return function
		self.pensieve.store(
			key='summary',
			precursors=[
				value for memory_dictionary in memory_list for key, value in memory_dictionary.items() if key != 'column'
			],
			function=create_summary(memory_list=memory_list)
		)

