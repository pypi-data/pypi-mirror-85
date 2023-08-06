from slytherin.collections import create_grid
import random
from pandas import DataFrame
from sklearn import gaussian_process


def get_values_from_range(start, end, num_digits):
	result = []
	x = start
	step = 1/(10**num_digits)
	while x <= end:
		result.append(round(x, num_digits))
		x += step
	return result


def get_all_points(parameter_ranges, parameter_values, num_rounding_digits):
	parameter_range_values = {
		key: get_values_from_range(start=range_tuple[0], end=range_tuple[1], num_digits=num_rounding_digits)
		for key, range_tuple in parameter_ranges.items()
	}
	parameters = create_grid({**parameter_range_values, **parameter_values})
	return parameters


def get_minimization_points(
		parameter_ranges, parameter_values, num_random_points, num_rounding_digits, seed, max_tries=10
):
	all_points = []
	tries = 0
	while len(all_points) < num_random_points and tries <= max_tries:

		all_points = get_all_points(
			parameter_ranges=parameter_ranges, parameter_values=parameter_values,
			num_rounding_digits=num_rounding_digits + tries
		)
		tries += 1
		if len(parameter_ranges) == 0:
			break

	if seed is not None:
		random.seed(seed)
	random.shuffle(all_points)
	return all_points[:num_random_points]
