from sklearn.linear_model import LinearRegression
from datetime import date, datetime
from chronometry import get_elapsed
import numpy as np

class Point:
	def __init__(self, x, y):
		if isinstance(x, (int, float)):
			self._x_type = 'numeric'
			self._reference = None
		elif isinstance(x, (datetime)):
			self._x_type = 'seconds'
			self._reference = datetime(2000, 1, 1)
		elif isinstance(x, (date)):
			self._x_type = 'days'
			self._reference = datetime(2000, 1, 1)

		else:
			raise TypeError(f'x: {x} is a {type(x).__name__} but x can be numeric, time, or date.')

		self._x = None
		self._original_x = None

		self.x = x
		self._y = y
		self._dy = None

	_STATE_VARIABLES = ['_x_type', '_reference', '_x', '_original_x', '_y', '_dy']

	def __hash__(self):
		return hash((self._original_x, self._y))

	def __getstate__(self):
		return {name: getattr(self, name) for name in self._STATE_VARIABLES}

	def __setstate__(self, state):
		for name, value in state.items():
			setattr(self, name, value)

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, x):
		self._original_x = x
		if self._x_type == 'numeric':
			self._x = x
		elif self._x_type == 'seconds':
			self._x = get_elapsed(start=self._reference, end=x, unit='second')
		elif self._x_type == 'days':
			self._x = get_elapsed(start=self._reference, end=x, unit='day')

	@property
	def y(self):
		return self._y

	@property
	def dy(self):
		return self._dy


	def __repr__(self):
		return f'({self._original_x}, {self.y})'

	def get_derivative(self, previous_point):
		"""
		:type previous_point: Point
		:rtype: float or str or None
		"""
		if self._x_type != previous_point._x_type:
			raise TypeError(f'cannot get derivative of two different x types: {self._x_type} and {previous_point._x_type}')
		if self.x == previous_point.x:
			if self.y > previous_point.y:
				return '+inf'
			elif self.y < previous_point.y:
				return '-inf'
			else:
				return None
		return (self.y - previous_point.y)/(self.x - previous_point.x)

	def __lt__(self, other):
		return self.x < other.x

	def __gt__(self, other):
		return self.x > other.x

	def __le__(self, other):
		return self.x <= other.x

	def __ge__(self, other):
		return self.x >= other.x

	def derivative_is_numeric(self):
		return self.dy is not None and not isinstance(self.dy, str)


def get_sign(x):
	if x > 0:
		return 1
	elif x < 0:
		return -1
	else:
		return 0


class Trend:
	def __init__(self, x=None, y=None, points=None):
		"""
		:type x: list[float] or NoneType
		:type y: list[float] or NoneType
		:type points: list[Point] or NoneType
		"""
		if points is None:
			if x is None or y is None:
				raise ValueError('either points or x and y should be provided!')
			points = [Point(x=x_i, y=y_i) for x_i, y_i in zip(x, y)]
			sorted_points = sorted(points)
		else:
			if x is not None or y is not None:
				raise ValueError('either points or x and y but not all of them should be provided!')
			sorted_points = sorted(points)

		x = [point.x for point in sorted_points]
		y = [point.y for point in sorted_points]

		for i in range(1, len(sorted_points)):
			point = sorted_points[i]
			previous_point = sorted_points[i - 1]
			point._dy = point.get_derivative(previous_point=previous_point)
		if len(sorted_points) > 1:
			if sorted_points[0].dy is None:
				sorted_points[0]._dy = sorted_points[1].dy

		if len(sorted_points) < 1:
			raise ValueError('trend is empty!')
		self._points = sorted_points
		self._linear = LinearRegression()
		self._derivative_linear = LinearRegression()

		if len(self._points) > 1:
			X = np.array(x).reshape((-1, 1))
			Y = np.array(y)
			self._linear.fit(X, Y)

			X2 = np.array([p.x for p in sorted_points if p.derivative_is_numeric()]).reshape((-1, 1))
			DY = np.array([p.dy for p in sorted_points if p.derivative_is_numeric()])
			self._derivative_linear.fit(X2, DY)

	def __getstate__(self):
		return {'_points': self._points, '_linear': self._linear, '_derivative_linear': self._derivative_linear}

	def __setstate__(self, state):
		for name, value in state.items():
			setattr(self, name, value)

	def __repr__(self):
		return repr(self._points)

	@property
	def points(self):
		return self._points

	@property
	def x_type(self):
		if len(self._points) > 0:
			return self._points[-1]._x_type
		else:
			return None

	def get_index(self, point):
		"""
		:type point: Point
		:rtype: int
		"""
		return self._points.index(point)

	def __getitem__(self, item):
		"""
		:type item: int
		:rtype: Point
		"""
		return self._points[item]

	@property
	def num_points(self):
		"""
		:rtype: int
		"""
		return len(self._points)

	@property
	def length(self):
		"""
		:rtype: int or float
		"""
		if self.num_points > 0:
			return self._points[-1].x - self._points[0].x
		else:
			return 0

	@property
	def sections(self):
		sections = {}
		section_number = 0
		for point in self._points:
			if point.dy is None:
				section_number += 1
			elif section_number not in sections:
				sections[section_number] = [point]
			elif get_sign(point.dy) == get_sign(sections[section_number][0].dy):
				sections[section_number].append(point)
			else:
				section_number += 1
				if section_number in sections:
					raise KeyError(f'{section_number} should not exist here!')
				sections[section_number] = [point]

		return [Trend(points=sections[section_number]) for section_number in sorted(sections.keys())]

	@property
	def minimums(self):
		minimum = min(self._points, key=lambda x: x.y)
		return [point for point in self._points if point.y == minimum.y]

	@property
	def maximums(self):
		maximum = max(self._points, key=lambda x: x.y)
		return [point for point in self._points if point.y == maximum.y]

	@property
	def a(self):
		try:
			return self._linear.coef_[0]
		except Exception as e:
			print(f'exception for:\n', self)
			raise e

	slope = a

	@property
	def b(self):
		try:
			return self._linear.intercept_
		except Exception as e:
			print(f'exception for:\n', self)
			raise e

	intercept = b

	@property
	def a_derivative(self):
		try:
			return self._derivative_linear.coef_[0]
		except Exception as e:
			print(f'exception for:\n', self)
			raise e

	@property
	def b_derivative(self):
		try:
			return self._derivative_linear.intercept_
		except Exception as e:
			print(f'exception for:\n', self)
			raise e

	def get_type(self, x=None, sensitivity=1e-6):
		if x is None:
			slope = self.a
		else:
			slope = self._derivative_linear.predict(X=x)

		if abs(slope) < sensitivity:
			if abs(self.a_derivative) < sensitivity:
				return 'stable'
			elif self.a_derivative > 0:
				return 'valley'
			else:
				return 'peak'

		elif slope > 0:
			if abs(self.a_derivative) < sensitivity:
				return 'constant_growth'
			elif self.a_derivative > 0:
				return 'accelerating_growth'
			else:
				return 'decelerating_growth'

		else:
			if abs(self.a_derivative) < sensitivity:
				return 'constant_decline'
			elif self.a_derivative > 0:
				return 'decelerating_decline'
			else:
				return 'accelerating_decline'

	def is_accelerating(self, x=None):
		return self.get_type(x=x).startswith('accelerating')

	def is_decelerating(self, x=None):
		return self.get_type(x=x).startswith('decelerating')

	def is_growing(self, x):
		return self.get_type(x=x).endswith('growth')

	def is_declining(self, x):
		return self.get_type(x=x).endswith('decline')
