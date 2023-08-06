import re


class MainEffect:
	def __init__(self, formula, p=None, coefficient=None):
		self._formula = formula.strip()
		self._p = p
		self._coefficient = coefficient
		search_result = re.search('^C\((.*)\)\[(.*)\]$', self._formula)
		self._level = None
		self._relative = None
		if search_result:
			self._type = 'categorical'
			self._name = search_result.group(1)
			self._level = search_result.group(2)
			if self._level.startswith('T.'):
				self._level = self._level[2:]
				self._relative = True

			else:
				self._relative = False

		elif formula.lower() == 'intercept':
			self._type = 'intercept'
			self._name = 'intercept'

		else:
			self._type = 'numeric'
			self._name = self._formula

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return False
		return self.formula == other.formula

	def __lt__(self, other):
		return self.name < other.name

	def __gt__(self, other):
		return self.name > other.name

	def __le__(self, other):
		return self.name <= other.name

	def __ge__(self, other):
		return self.name >= other.name

	def __hash__(self):
		return hash(self.name)

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.__str__()

	@property
	def coefficient(self):
		return self._coefficient

	@property
	def p(self):
		return self._p

	@property
	def num_interactions(self):
		return 0

	def get_variable(self, index, missing=None):
		if index == 0:
			return self
		else:
			return missing

	@property
	def formula(self):
		return self._formula

	def represent(self, multiply_symbol=''):
		return self.formula

	@property
	def type(self):
		return self._type

	@property
	def name(self):
		return self._name

	@property
	def categorical_level(self):
		return self._level

	@property
	def relative(self):
		return self._relative
