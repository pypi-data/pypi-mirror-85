from pandas import DataFrame


def sum_text(x):
	text = ''.join(x.values)
	text = '\n'.join(text.split('\n'))
	text = ' '.join(text.split(' '))
	return text


def merge_texts(data):
	"""
	:type data: DataFrame
	:rtype: DataFrame
	"""
	data = data.copy()
	data['previous_depth'] = data['depth'].shift()
	data['previous_parent_id'] = data['parent_id'].shift()
	data['is_break'] = data['text'] == '\n'
	data['previous_is_break'] = data['is_break'].shift().fillna(False)
	data['new_paragraph'] = data['previous_depth'].isna() | \
							(data['depth'] != data['previous_depth']) | \
							(data['is_break'] & data['previous_is_break']) | \
							(data['previous_parent_id'] != data['parent_id'])
	data['paragraph_index'] = data['new_paragraph'].cumsum()

	important_columns = ['font_family', 'font_size', 'is_bold', 'is_italic']
	text = data[['paragraph_index', 'text']].groupby('paragraph_index').agg(sum_text).reset_index()
	the_rest = data[['paragraph_index'] + important_columns].groupby('paragraph_index', as_index=False).first()

	result = the_rest.merge(text, on='paragraph_index', how='outer').sort_values('paragraph_index')
	result['text'] = result['text'].str.strip()
	result = result[result['text'] != '']

	return result
