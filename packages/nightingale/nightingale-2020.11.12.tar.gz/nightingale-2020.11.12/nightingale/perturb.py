from ravenclaw import get_numeric_columns, is_numeric
from chronometry.progress import ProgressBar
from pandas import concat
from pensieve import Pensieve


def perturb_numeric_column(data, column, delta):
	data = data.copy()
	data['perturbed_column'] = column
	data['original_value'] = data[column].values
	data['perturbation'] = delta
	data[column] = data['original_value'] + delta
	return data

def perturb_categorical_column(data, column, category):
	data = data.copy()
	data['perturbed_column'] = column
	data['original_value'] = data[column].values
	data['perturbation'] = data[column].apply(lambda x: f'{x} -> {category}')
	data[column] = category
	return data

def perturb(data, numeric_perturbation, columns=None, transformation=None, function=None, echo=1):
	"""
	perturbs a dataframe by adding and subtracting delta from one or all numeric columns
	:type data: pandas.DataFrame
	:type numeric_perturbation: float or list[float] or dict[str, float] or dict[str, list[float]]
	:type columns: NoneType or str or list[str]
	:type echo: bool or int or interaction.ProgressBar
	:type transform: NoneType or callable
	:type function: NoneType or callable
	:return:
	"""
	pensieve = Pensieve()
	try:

		data = data.copy()
		data['perturbation_id'] = range(len(data))
		pensieve['data'] = data

		pensieve['transformation'] = transformation

		pensieve['input_columns'] = columns
		pensieve['numeric_columns'] = lambda data, input_columns: [
			column
			for column in (input_columns or data.columns)
			if is_numeric(data[column])
		]
		pensieve['categorical_columns'] = lambda data, input_columns: [
			column
			for column in (input_columns or data.columns)
			if not is_numeric(data[column])
		]

		pensieve['input_perturbation'] = numeric_perturbation
		def get_perturbation(input_perturbation, columns):
			if not isinstance(input_perturbation, dict):
				perturbation_dictionary = {column: input_perturbation for column in columns}
			else:
				perturbation_dictionary = {column: input_perturbation[column] for column in columns if column in input_perturbation}

			return {
				key: value if isinstance(value, (list, tuple, set)) else [value]
				for key, value in perturbation_dictionary.items()
			}
		pensieve.store(key='perturbation', function=get_perturbation)

		def perturb_data(data, perturbation):
			list_of_data = []
			progress_bar = ProgressBar(total=len(perturbation), echo=echo)
			progress = 0
			for column, perturbation_list in perturbation.items():
				progress_bar.show(amount=progress, text=column)
				for delta in perturbation_list:
					list_of_data.append(perturb_numeric_column(data=data, column=column, delta=delta))
				progress += 1
			data = concat(list_of_data)
			progress_bar.show(amount=progress)
			return data
		pensieve.store(key='perturbed_data', function=perturb_data)

		def transform_data(data, transformation):
			data = data.copy()
			if transformation is None:
				def transformation(x):
					return x
			result = transformation(data.drop(columns='perturbation_id'))
			if len(result) != len(data):
				raise RuntimeError(f'transformation changes data length from {len(data)} to {len(result)}')
			result['perturbation_id'] = data['perturbation_id']
			return result
		pensieve.store(key='data__transformed', function=transform_data)

		pensieve.store(
			key='perturbed_data__transformed',
			function=lambda perturbed_data, transformation: transform_data(
				data=perturbed_data, transformation=transformation
			)
		)

		pensieve.store(
			key='original_columns',
			function=lambda data__transformed: [
				column for column in data__transformed.columns if column != 'perturbation_d'
			]
		)

		pensieve['function'] = function

		def apply_function(data, function, original_columns):
			result = data.copy()
			if function is not None:
				result['function_result'] = function(result[original_columns])
			return result
		pensieve.store(
			key='function_result',
			function=lambda data__transformed, function, original_columns: apply_function(
				data=data__transformed,
				function=function,
				original_columns=original_columns
			)
		)
		pensieve.store(
			key='perturbed__function_result',
			function=lambda perturbed_data__transformed, function, original_columns: apply_function(
				data=perturbed_data__transformed,
				function=function,
				original_columns=original_columns
			)
		)

		def compare(perturbed__function_result, function_result):
			perturbed__function_result = perturbed__function_result.copy()
			if 'function_result' in function_result.columns:
				function_result = function_result[['perturbation_id', 'function_result']]
				function_result = function_result.rename(columns={'function_result': 'original_function_result'})

				perturbed__function_result = perturbed__function_result.rename(
					columns={'function_result': 'perturbed_function_result'}
				)
				comparison = perturbed__function_result.merge(right=function_result, on='perturbation_id', how='left')
				if is_numeric(comparison['perturbed_function_result']):
					comparison['function_perturbation'] = comparison['perturbed_function_result'] - comparison['original_function_result']
				else:
					comparison['function_perturbation'] = comparison['perturbed_function_result'] != comparison['original_function_result']
				return comparison
			else:
				return perturbed__function_result



		pensieve.store(key='comparison', function=compare)
	except Exception as e:
		print(e)

	return pensieve
