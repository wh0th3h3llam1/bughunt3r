from django import template

register = template.Library()

@register.filter(name='get_last_item')
def get_last_item(text):
	if isinstance(text, str):
		return text.split(' ')[-1]
	return False