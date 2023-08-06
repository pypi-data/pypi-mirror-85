from pandas import DataFrame
from copy import deepcopy
from functools import wraps


def get_values_from_range(start, end, num_digits):
	result = []
	x = start
	step = 1/(10**num_digits)
	while x <= end:
		result.append(round(x, num_digits))
		x += step
	return result


def create_mimic(function, model, known_points, known_results, unknown_points, fixed_parameters=None, return_results=False):
	"""
	:type function: callable 
	:rtype: callable or tuple(callable, list)
	"""
	fixed_parameters = fixed_parameters or {}
	results_of_unknown = [function(**unknown_point, **fixed_parameters) for unknown_point in unknown_points]

	X = DataFrame.from_records(list(known_points) + list(unknown_points))
	y = list(known_results) + results_of_unknown

	new_model = deepcopy(model)
	new_model.fit(X, y)

	x_columns = X.columns

	@wraps(function)
	def mimic(**kwargs):
		for key in set(kwargs.keys()).union(set(x_columns)):
			if key not in x_columns:
				raise KeyError(f'{key} is does not exist in the original function')
			elif key not in kwargs.keys():
				raise KeyError(f'{key} is missing from the arguments')

		X = DataFrame.from_records([kwargs])
		return new_model.predict(X)[0]

	if return_results:
		return mimic, results_of_unknown
	else:
		return mimic

