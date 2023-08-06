from .LogisticRegression import LogisticRegression
from .OLS import OLS
from .GEE import GEE, LogisticGEE


def get_grouped_regression(data, formula, groups, regression_type):
	data = data.copy()
	if isinstance(groups, str):
		data['_groups_'] = data[groups]
	else:
		data['_groups_'] = data.apply(
			axis=1,
			func=lambda x: hash(tuple([
				x[column] for column in groups
			]))
		)
	groups = '_groups_'

	if regression_type == 'linear':
		model = GEE(formula=formula, data=data, groups=groups)
	else:
		model = LogisticGEE(formula=formula, data=data, groups=groups)
	return model

def get_regression_model(formula, data, regression_type, groups, eliminate=False, echo=1):

	if groups is None or groups == []:
		if regression_type == 'linear':
			model = OLS(data=data, formula=formula)
		else:
			model = LogisticRegression(data=data, formula=formula)
	else:
		model = get_grouped_regression(
			data=data, formula=formula, groups=groups, regression_type=regression_type
		)

	if not eliminate:
		return model
	else:
		return model.eliminate(num_rounds=None, echo=echo)
