from django import template

register = template.Library()

@register.filter
def multiply_and_round(value, arg):
    """Multiplies the value by the arg and rounds the result to 2 decimal places."""
    return round(value * arg, 2)