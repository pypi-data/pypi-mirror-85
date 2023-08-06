from scipy import optimize
import numpy as np
import warnings


def bound_it(x, lower, upper):
	if lower is not None and upper is not None and lower > upper:
		lower, upper = upper, lower

	if lower is not None:
		x = max(x, lower)
	if upper is not None:
		x = min(x, upper)
	return x


class MinimizationResult:
	def __init__(self, result, arg_names, bounds=None, integers=None):
		self._result = result
		self._arg_names = arg_names
		self._bounds = bounds
		self._integers = integers

	@property
	def args(self):
		"""
		:rtype: dict
		"""
		if len(self._arg_names) == 1 and self._result.x.size == 1:
			result = {self._arg_names[0]: self._result.x.flat[0]}
		else:
			try:
				result = {key: value for key, value in zip(self._arg_names, self._result.x.flat)}
			except TypeError:

				display(self._arg_names, self._result.x)
				raise

		if self._integers:
			for key in self._integers:
				result[key] = int(round(result[key]))

		if self._bounds:
			for key in self._bounds:
				value = result[key]
				lower, upper = self._bounds[key]
				result[key] = bound_it(x=value, lower=lower, upper=upper)

		return result

	def __repr__(self):
		return repr(self.args)

	def __str__(self):
		return self.__repr__()


def penalize(x, upper, lower):
	"""
	produces a penalty relative to how much x is above the upper or below lower bound. maximum value is 2
	:param x:
	:param upper:
	:param lower:
	:return:
	"""
	if lower is not None and upper is not None and lower > upper:
		lower, upper = upper, lower
	u = 0
	l = 0
	if upper is not None and x > upper:
		u += 1 - (1 / ((x - upper)**2 + 1))
	if lower is not None and x < lower:
		l += 1 - (1 / ((x - lower)**2 + 1))
	return u + l


def minimize(
		function, args_to_optimize, initial_args, bounds=None, integers=None,
		constraint_penalty=1e3, constraints=None, method='Powell', max_iterations=None, max_evaluations=None,
		**kwargs
):
	"""
	a wrapper for the scipy minimize function that is easier to use because it uses dictionaries rather than lists
	:param callable				function: a function to be minimized
	:param list[str] 			args_to_optimize: list of function arguments to be optimized
	:param dict[str] 			initial_args: dictionary of initial values of the arguments
	:param dict 				kwargs: extra arguments for the scipy minimize method
	:param dict[str, tuple] 	bounds: dictionary of boundaries of the arguments, None means infinity
	:param list[str] 			integers: list of arguments that should be kept as integers
	:rtype: MinimizationResult
	"""
	constant_args = {key: value for key, value in initial_args.items() if key not in args_to_optimize}

	def new_function(x):
		new_kwargs = {key: value for key, value in zip(args_to_optimize, x)}
		new_kwargs.update(constant_args)
		penalty = 0

		if bounds is not None:
			for key in bounds:
				value = new_kwargs[key]
				lower, upper = bounds[key]
				new_kwargs[key] = bound_it(x=value, lower=lower, upper=upper)
				penalty += penalize(x=value, upper=upper, lower=lower)

		if integers is not None:
			for key in integers:
				try:
					new_kwargs[key] = int(round(new_kwargs[key]))
				except ValueError:
					pass

		return function(**new_kwargs) + penalty * constraint_penalty

	if integers is not None:
		integer_constraints = {
			'type': 'eq',
			'fun': lambda x: max([
				x[i] - int(x[i]) if key in integers else 0
				for i, key in enumerate(args_to_optimize)
			])
		}
		if constraints is None:
			constraints = (integer_constraints,)
		else:
			constraints = tuple(list(constraints) + [integer_constraints])

	x0 = np.array([initial_args[key] for key in args_to_optimize])

	fprime = lambda x: optimize.approx_fprime(x, new_function, 0.01)
	if max_iterations is not None or max_evaluations is not None:
		options = {}
		if max_iterations is not None:
			options['maxiter'] = max_iterations
		if max_evaluations is not None:
			options['maxfev'] = max_evaluations
	else:
		options = None

	try:
		with warnings.catch_warnings():
			warnings.simplefilter('ignore')
			result = optimize.minimize(
				fun=new_function, x0=x0, constraints=constraints, jac=fprime, method=method,
				options=options,
				**kwargs
			)
	except:
		with warnings.catch_warnings():
			warnings.simplefilter('ignore')
			result = optimize.minimize(
				fun=new_function, x0=x0, constraints=constraints, jac=fprime, method='Powell',
				options=options,
				**kwargs
			)

	return MinimizationResult(result=result, arg_names=args_to_optimize, bounds=bounds, integers=integers)
