from .minimize import minimize
from .create_mimic import create_mimic


def fast_minimize(
		function, args_to_optimize, model, random_points, num_starting_points, fixed_parameters=None, num_repeats=1,
		bounds=None, integers=None,
		constraint_penalty=1e3, constraints=None, method='Powell', max_iterations=None, max_evaluations=None,
		**kwargs
):
	known_points = []
	known_results = []
	unknown_points = random_points[:num_starting_points]
	remaining_random_points = random_points[num_starting_points:]
	fixed_parameters = fixed_parameters or {}
	minimization = None

	for i in range(num_repeats):
		mimic, unknown_results = create_mimic(
			function=function,
			model=model,
			known_points=known_points,
			known_results=known_results,
			unknown_points=unknown_points,
			fixed_parameters=fixed_parameters,
			return_results=True
		)
		known_points += unknown_points
		known_results += unknown_results

		the_zip = list(sorted(zip(known_points, known_results), key=lambda pair: pair[1]))
		best_point = the_zip[0][0]
		#print('best_point:', best_point, 'result:', the_zip[0][1])
		minimization = minimize(
			function=mimic, args_to_optimize=args_to_optimize, initial_args=best_point,
			bounds=bounds, integers=integers,
			constraints=constraints, constraint_penalty=constraint_penalty, method=method,
			max_iterations=max_iterations, max_evaluations=max_evaluations, **kwargs
		)
		#print('minimization:', minimization)
		minimization_point = minimization.args
		minimization_result = function(**minimization_point, **fixed_parameters)
		known_points.append(minimization_point)
		known_results.append(minimization_result)
		if len(remaining_random_points) > 0:
			random_point = remaining_random_points.pop()
			random_result = function(**random_point, **fixed_parameters)

			#if minimization_result < random_result:
			#	print('minimization is smaller')
			#else:
			#	print('random is smaller')
			known_points.append(random_point)
			known_results.append(random_result)
		else:
			pass
			#print('ran out of random points')
		unknown_points = []

	return minimization#, known_points, known_results
