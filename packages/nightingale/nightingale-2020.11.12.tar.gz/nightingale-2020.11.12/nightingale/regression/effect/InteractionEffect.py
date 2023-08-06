from .MainEffect import MainEffect


class InteractionEffect:
	def __init__(self, formula, p=None, coefficient=None):
		formula = formula.replace(':', "*")
		self._main_effects = sorted([MainEffect(formula=x) for x in formula.split('*')], key=lambda x: x.formula)
		self._p = p
		self._coefficient = coefficient

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return False
		elif self.num_interactions != other.num_interactions:
			return False
		return self.formula == other.formula

	def __lt__(self, other):
		return (self.num_interactions, self.name) < (other.num_interactions, other.name)

	def __gt__(self, other):
		return (self.num_interactions, self.name) > (other.num_interactions, other.name)

	def __le__(self, other):
		return (self.num_interactions, self.name) <= (other.num_interactions, other.name)

	def __ge__(self, other):
		return (self.num_interactions, self.name) >= (other.num_interactions, other.name)

	def __hash__(self):
		return hash(self.name)

	def contains(self, main_effect):
		for x in self.main_effects:
			if x.formula == main_effect.formula:
				return True
		return False

	@property
	def main_effects(self):
		"""
		:rtype: list[MainEffect]
		"""
		return self._main_effects

	@property
	def coefficient(self):
		return self._coefficient

	@property
	def p(self):
		return self._p

	@property
	def num_interactions(self):
		return len(self.main_effects) - 1

	def get_variable(self, index, missing=None):
		if index < len(self.main_effects):
			return self.main_effects[index]
		else:
			return missing

	@property
	def type(self):
		"""
		:rtype: str
		"""
		return '-'.join(sorted([main_effect.type for main_effect in self.main_effects]))

	@property
	def formula(self):
		"""
		:rtype: str
		"""
		return self.represent(multiply_symbol='*')

	def represent(self, multiply_symbol='×'):
		"""
		:rtype: str
		"""
		return f' {multiply_symbol} '.join([main_effect.formula for main_effect in self.main_effects])

	@property
	def name(self):
		"""
		:rtype: str
		"""
		return ' × '.join([main_effect.name for main_effect in self.main_effects])

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.__repr__()

	@property
	def categorical_level(self):
		return None

	@property
	def relative(self):
		return None

