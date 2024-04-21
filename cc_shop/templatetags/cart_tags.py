from django import template

register = template.Library()

@register.filter
def multiply_and_round(value, arg):
    # Multiply the value by the arg and round the result to 2 decimal places
    return round(value * arg, 2)