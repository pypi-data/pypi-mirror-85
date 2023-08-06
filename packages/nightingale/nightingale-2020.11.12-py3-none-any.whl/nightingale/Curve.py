import numpy as np
from scipy.optimize import curve_fit
from slytherin.collections import Series


class Curve:
	def __init__(self, function):
		self._optimal_parameters = None
		self._parameter_covariance = None
		self._fit_successful = None
		self._function = function
		self._curve = None

	def fit(self, x, y, parameter_lower_bounds=None, parameter_upper_bounds=None):
		x = np.array(x)
		y = np.array(y)

		parameter_lower_bounds = parameter_lower_bounds or -np.inf
		parameter_upper_bounds = parameter_upper_bounds or np.inf

		try:
			self._optimal_parameters, self._parameter_covariance = curve_fit(
				self._function, x, y, bounds=(parameter_lower_bounds, parameter_upper_bounds)
			)
			self._curve = lambda x: self._function(x, *self.optimal_parameters)
			self._fit_successful = True

		except Exception as e:
			self._fit_successful = False
			raise e

		return self._fit_successful

	@property
	def optimal_parameters(self):
		return self._optimal_parameters

	def predict(self, x):
		if self._fit_successful is None:
			raise RuntimeError('Curve is not fit yet!')

		elif not self._fit_successful:
			raise RuntimeError('Curve fit was unsuccessful!')

		else:
			return_type = 'list' if isinstance(x, list) else 'not_list'
			x = np.array(x)
			y = self._curve(x)
			if return_type == 'list':
				y = list(y)
			return y

	def plot(self, x, y=None):
		try:
			import matplotlib.pyplot as plt
		except ModuleNotFoundError:
			print('matplotlib is not installed')
			return False

		smooth_x = Series(start=min(x), end=max(x), step=(max(x) - min(x))/(10*len(x))).list
		plt.plot(smooth_x, self.predict(smooth_x), color='lightcoral')
		if y is not None:
			plt.plot(x, y, 'ro', color='navy')
		else:
			plt.plot(x, self.predict(x), 'ro', color='lightcoral')
