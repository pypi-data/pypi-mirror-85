import re


_first_cap_re = re.compile('(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')
def convert_camel_to_snake(string):
	s1 = _first_cap_re.sub(r'\1_\2', string)
	result = _all_cap_re.sub(r'\1_\2', s1).lower()
	result = re.sub(pattern='_+', repl="_", string=result)
	#print(manipulation, result)
	return result