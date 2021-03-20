from django import template

register = template.Library()

@register.filter(name='get_first_item')
def get_first_item(text):
	if isinstance(text, str):
		return text.split(' ')[-1]
	if isinstance(text, list) or isinstance(text, set) or isinstance(text, tuple):
		return dict(text[0])
	return False