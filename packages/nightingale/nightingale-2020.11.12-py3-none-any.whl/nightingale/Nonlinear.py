from sklearn.linear_model import LinearRegression
from scipy.optimize import minimize
import numpy as np
from numpy import ndarray

class Nonlinear:
	def __init__(self, transform):
		"""
		:param callable transform: transformation function applied to x with an optional parameter c
		"""
		self._transform = transform
		self._function = None

	def fit(self, x, y, c0, optimization_method='Nelder-Mead'):
		"""
		this function fits the best function of form:
		y = a.f(x, c) + b
		:param list[float] or list[int] x: independent variable
		:param list[float] or list[int] y: dependent variable
		:param callable or NoneType transformation: a function to transform x
		:param float or int or ndarray c0: first guess for best c
		:param str optimization_method: method used for optimizing c
		:rtype: callable
		"""
		self._function = fit_nonlinear(
			x=x, y=y, transform_x=self._transform, transform_x_params=c0, optimization_method=optimization_method
		)

	train = fit

	@property
	def a(self):
		if self._function is None:
			raise RuntimeError('model is not trained yet!')
		return self._function.a

	@property
	def b(self):
		if self._function is None:
			raise RuntimeError('model is not trained yet!')
		return self._function.b

	@property
	def c(self):
		if self._function is None:
			raise RuntimeError('model is not trained yet!')
		return self._function.c

	def predict(self, x):
		if self._function is None:
			raise RuntimeError('model is not trained yet!')

		return self._function(x)


def fit_nonlinear(
		x, y,
		transform_x=None, transform_x_params=None,
		transform_y=None, transform_y_params=None,
		optimization_method='Nelder-Mead'
):
	"""
	this function fits the best function of form:
	y = a.f(x, c) + b
	:param list[float] or list[int] x: independent variable
	:param list[float] or list[int] y: dependent variable
	:param callable or NoneType transform_x: a function to transform x
	:param callabel or NoneType transform_y: a function to transform y
	:param float or int or list[float] transform_x_params: first guess for best parameters of transform_x
	:param float or int or list[float] transform_y_params: first guess for best parameters of transform_y
	:param str optimization_method: method used for optimizing
	:rtype: callable
	"""

	def get_trend_function(_x, _y, _transform_x, _transform_x_params):
		if _transform_x is None:
			u = _x.copy()
		elif _transform_x_params is None:
			u = [_transform_x(i) for i in _x]
		else:
			u = [_transform_x(i, _transform_x_params) for i in _x]

		u = np.array(u).reshape((-1, 1))
		_y = np.array(_y)

		model = LinearRegression()
		model.fit(u, _y)
		a = model.coef_[0]
		b = model.intercept_

		def func(x):
			if isinstance(x, list):
				return [a * _transform_x(x_i, _transform_x_params) + b for x_i in x]
			else:
				return a * _transform_x(x, _transform_x_params) + b

		return a, b, func

	def cost(cost_transform_x_params, cost_x, cost_y, cost_transform_x):
		a, b, f = get_trend_function(_x=cost_x, _y=cost_y, _transform_x=cost_transform_x, _transform_x_params=cost_transform_x_params)
		return sum([(cost_y_i - f(cost_x_i)) ** 2 for cost_x_i, cost_y_i in zip(cost_x, cost_y)])

	if transform_x is None:
		transform_x_params = None
	else:
		result = minimize(
			lambda c: cost(cost_transform_x_params=c, cost_x=x, cost_y=y, cost_transform_x=transform_x),
			transform_x_params,
			method=optimization_method
		)
		transform_x_params = result.x

	a, b, f = get_trend_function(_x=x, _y=y, _transform_x=transform_x, _transform_x_params=transform_x_params)
	f.a = a
	f.b = b
	f.c = transform_x_params
	return f
