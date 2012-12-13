from django import template

register = template.Library()

@register.filter
def keyvalue(dict, key): 
	if dict.has_key(key):
		return dict[key]
	return ''