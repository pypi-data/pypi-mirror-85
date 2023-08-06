from pandas import DataFrame

def convert_simple_table_to_dataframe(simple_table, header=True):
	list_of_lists = simple_table.data

	if header:
		header = list_of_lists[0]
		column_names = header[1:]
		body = list_of_lists[1:]
	else:
		column_names = None
		body = list_of_lists


	index = [l[0] for l in body]
	data = [l[1:] for l in body]
	df = DataFrame.from_records(data=data, columns=column_names, index=index)

	return df
