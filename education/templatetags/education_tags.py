from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Return dictionary[key], safe for missing keys."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def replace(value, args):
    """Replace all occurrences of old with new. Usage: {{ value|replace:"old:new" }}"""
    if ':' not in str(args):
        return value
    old, new = str(args).split(':', 1)
    return str(value).replace(old, new)
