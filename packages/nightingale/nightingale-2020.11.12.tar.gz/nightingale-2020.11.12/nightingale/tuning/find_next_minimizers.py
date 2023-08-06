


def create_minimization_data(function, known_points, known_results, unknown_points, fixed_parameters):
	X = DataFrame.from_records(known_points + unknown_points)
	y = known_results + [function(**point, **fixed_parameters) for point in unknown_points]
	return X, y


def build_gaussian():
	return gaussian_process.GaussianProcessRegressor()


def sort_points(function, known_points, known_results, unknown_points, fixed_parameters, num_runs=1, model=None):
	known_points = known_points or []
	known_results = known_results or []

	num_runs = min(num_runs, len(unknown_points))
	if num_runs < 1:
		raise ValueError('no unknown point')

	new_unknown_points = unknown_points[num_runs:]

	new_known_points = unknown_points[:num_runs]
	new_known_results = [function(**point, **fixed_parameters) for point in new_known_points]
	model = model or gaussian_process.GaussianProcessRegressor()
	X_training = DataFrame.from_records(known_points + new_known_points)
	y_training = known_results + new_known_results
	model.fit(X_training, y_training)

	if len(new_unknown_points) > 0:
		X_test = DataFrame.from_records(new_unknown_points)
		try:
			y_test = model.predict(X_test)
		except Exception as e:
			display(X_test)
			raise e

		new_unknown_points = [x for _,x in sorted(zip(y_test, new_unknown_points), key=lambda pair: pair[0])]

	return {'known_points': new_known_points, 'known_results': new_known_results, 'unknown_points': new_unknown_points}



def minimize(
		function, model=None, parameter_ranges=None, parameter_values=None, fixed_parameters=None,
		num_starting_points=5, num_points_per_step=5, num_iterations=100,
		num_rounding_digits=6, seed=None
):
	"""
	:param callable function: function to be minimized
	:param dict[str, tuple] or NoneType parameter_ranges: parameters whose values should be chosen from a range
	:param dict[str, list] or NoneType parameter_values: parameters whose values should be chosen from a list
	:param dict[str, ] or NoneType fixed_parameters: parameters whose values are fixed
	:rtype: dict[str, ]
	"""
	parameter_ranges = parameter_ranges or {}
	parameter_values = parameter_values or {}
	fixed_parameters = fixed_parameters or {}

	points = get_random_points(
		parameter_ranges=parameter_ranges, parameter_values=parameter_values, num_random_points=num_iterations,
		num_rounding_digits=num_rounding_digits, seed=seed, max_tries=10
	)

	known = points[:num_starting_points]
	unknown = points[num_starting_points:]

	if















