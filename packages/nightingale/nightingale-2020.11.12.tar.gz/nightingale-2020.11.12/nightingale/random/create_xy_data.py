import pandas as pd
from random import sample, choice, random
from numpy.random import normal


def create_xy_data(
		num_rows=100, num_x_columns=10, correlation_ratio=0.5, correlation_noise=0.1, num_coefficients=5,
		interactions=True
):
	num_correlating_features = round(correlation_ratio * num_x_columns)
	num_independent_features = num_x_columns - num_correlating_features

	independent_columns = [f'x{i}' for i in range(1, num_independent_features + 1)]

	data = pd.DataFrame({
		column: normal(scale=1, size=num_rows)
		for column in independent_columns
	})

	correlating_columns = [f'x{i}' for i in range(num_independent_features + 1, num_x_columns + 1)]

	for column in correlating_columns:
		independent_column = choice(independent_columns)
		print(f'{column} correlates with {independent_column}')
		data[column] = data[independent_column] + normal(scale=correlation_noise, size=num_rows)

	coefficients = {
		column: random()
		for column in sample(independent_columns + correlating_columns, k=num_coefficients)
	}

	if interactions:
		interaction_coefficients = {
			(column_1, column_2): random() * 10
			for column_1 in sample(independent_columns + correlating_columns, k=round(num_coefficients ** 0.5))
			for column_2 in sample(independent_columns + correlating_columns, k=round(num_coefficients ** 0.5))
		}
	else:
		interaction_coefficients = {}

	data['y'] = normal(scale=correlation_noise * num_coefficients, size=num_rows)

	parts = []

	for column, coefficient in coefficients.items():
		data['y'] = data['y'].values + data[column].values * coefficient
		parts.append(f'{round(coefficient, 2)} {column}')

	for columns, coefficient in interaction_coefficients.items():
		column_1, column_2 = columns
		data['y'] = data['y'].values + data[column_1].values * data[column_2].values * coefficient
		parts.append(f'{round(coefficient, 2)} {column_1}.{column_2}')

	print(f'y = {" + ".join(parts)}')

	return data








