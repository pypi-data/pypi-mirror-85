import numpy as np
from sklearn.linear_model import LinearRegression

from .Curve import Curve
EPSILON = 1e-10


class Sigmoid(Curve):
	def __init__(self, x=None, y=None, a=None, b=None, c=None, check_slope=True):
		super().__init__(function=self._sigmoid)
		self._a = a
		self._b = b
		self._c = c
		self._slope = None
		if x is not None and y is not None:
			self.fit(x=x, y=y, check_slope=check_slope)

	def _sigmoid(self, x, a, b, c):
		a = self._a or a
		b = self._b or b
		c = self._c or c


		return a/(np.exp(-b*x + c) + 1)

	def fit(self, x, y, parameter_lower_bounds=None, parameter_upper_bounds=None, check_slope=True):
		x = np.array(x)
		y = np.array(y)

		linear = LinearRegression()
		linear.fit(X=x.reshape((-1, 1)), y=y)
		self._slope = linear.coef_[0]
		if check_slope and self._slope <=0:
			self._fit_successful = False
			return False

		parameter_lower_bounds = parameter_lower_bounds or [0, 0, -np.inf]
		parameter_upper_bounds = parameter_upper_bounds or [np.inf, np.inf, np.inf]
		if self._a:
			parameter_upper_bounds[0] = self._a + EPSILON
			parameter_lower_bounds[0] = self._a - EPSILON
		if self._b:
			parameter_upper_bounds[1] = self._b + EPSILON
			parameter_lower_bounds[1] = self._b - EPSILON
		if self._c:
			parameter_upper_bounds[2] = self._b + EPSILON
			parameter_lower_bounds[2] = self._b - EPSILON

		result = super().fit(x=x, y=y, parameter_lower_bounds=parameter_lower_bounds, parameter_upper_bounds=parameter_upper_bounds)

		if self._a:
			self._optimal_parameters[0] = self._a
		if self._b:
			self._optimal_parameters[1] = self._b
		if self._c:
			self._optimal_parameters[2] = self._c

		return result

	@property
	def a(self):
		return self._optimal_parameters[0]

	@property
	def b(self):
		return self._optimal_parameters[1]

	@property
	def c(self):
		return self._optimal_parameters[2]

	@property
	def parameters(self):
		return {'a': self.a, 'b': self.b, 'c': self.c}
