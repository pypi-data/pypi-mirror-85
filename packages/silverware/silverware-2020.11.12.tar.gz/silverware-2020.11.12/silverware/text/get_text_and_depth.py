import re
from .get_style import get_style


def get_raw_text(tag):
	"""
	:type tag: Tag
	:rtype: NoneType or str
	"""
	if tag.name == 'br':
		return '\n'

	elif hasattr(tag, 'text'):
		text = tag.text
		if text is None:
			return None
	else:
		text = str(tag)

	return text


def is_break(tag):
	return tag.name == 'br'


def has_children(tag):
	return len(get_children(tag=tag)) > 0


def has_no_children(tag):
	return len(get_children(tag=tag)) == 0


def get_children(tag):
	"""
	:type tag: Tag or list or tuple
	:rtype: NoneType or list[Tag]
	"""
	if isinstance(tag, (list, tuple)):
		return list(tag)

	if not hasattr(tag, 'children'):
		return []

	else:
		return [x for x in tag.children if x is not None and x != []]


def get_text_and_depth(tag, id, parent_id, depth, parent_style, parent_dna, parent_name, tag_name_counter):
	"""
	:param 	Tag 			tag: 				the html tag
	:param 	str 			id: 				the unique id of this element
	:param 	str 			parent_id: 			the id of the parent of this element
	:param 	int 			depth: 				the depth of the element
	:param 	dict 			parent_style: 		a dictionary that contains the style of the element (font size, etc.)
	:param 	str 			parent_dna: 		a string that tells what the ancestors of this element have been
	:param 	str 			parent_name: 		the name of the parent tag
	:param 	dict[str, int] 	tag_name_counter: 	a dictionary that keeps count of tag names
												to make sure unique names are generated for new elements
	:rtype: list[dict[str,]]
	"""
	parent_style = parent_style or {}
	style = get_style(tag=tag)
	# merge styles with priority given to style
	style = {**parent_style, **style}

	children = get_children(tag)
	tag_name = tag.name or 'text'

	if tag_name not in tag_name_counter:
		tag_name_counter[tag_name] = 0

	tag_name_counter[tag_name] += 1
	name = f'{tag_name}_{tag_name_counter[tag_name]}'
	if parent_dna == '':
		dna = tag_name
	else:
		dna = parent_dna + '.' + tag_name

	if len(children) == 0:
		text = get_raw_text(tag=tag)

		if re.search(r'^\s*Page \d+$', text):
			text = None

		if text is None or len(text) == 0:
			return []
		else:
			return [{
				'id': id,
				'name': name,
				'dna': dna,
				'parent_id': parent_id,
				'parent_name': parent_name,
				'parent_dna': parent_dna,
				'depth': depth, 'text': text, **style
			}]

	else:
		result = []

		if len(id) > 0:
			id_prefix = f'{id}.'
		else:
			id_prefix = ''

		max_child_id_width = len(str(len(children)))

		for index, child in enumerate(children):
			child_partial_id = str(index + 1).rjust(max_child_id_width, '0')

			child_text_and_depth = get_text_and_depth(
				tag=child,
				id=f'{id_prefix}{child_partial_id}',
				parent_id=id,
				depth=depth + 1,
				parent_style=style,
				parent_dna=dna,
				parent_name=name,
				tag_name_counter=tag_name_counter
			)
			result += child_text_and_depth

		return result
