from .Trend import Trend
from .Nonlinear import Nonlinear

import math

class LogarithmicGrowth(Trend):
	def __init__(self, timestamps, values):
		time_shift = 1-min(timestamps)
		super().__init__(x=timestamps, y=values)
		self._time_shift = time_shift

		if self.is_decelerating(x=max(timestamps)) or self.is_decelerating(x=None):
			self._model = Nonlinear(
				transform=lambda x, c: math.log(x+time_shift) - (x+time_shift)/c
			)
			self._model.fit(x=timestamps, y=values, c0=max(timestamps) + 1)
		else:
			self._model = None

	@property
	def capacity(self):
		if self._model is None:
			return None
		else:
			return self._model.predict(x=self._model.c)[0]

	@property
	def settling_time(self):
		if self._model is None:
			return None
		else:
			return self._model.c[0]

	def predict(self, x):
		if self._model is None:
			return None
		else:
			return self._model.predict(x=min(x, self.settling_time))
