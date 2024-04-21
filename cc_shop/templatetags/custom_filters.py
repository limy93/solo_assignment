from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    # Multiply the value: value * arg
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter(name='sum_cart_total')
def sum_cart_total(cart_items):
    # Calculate the sum of total prices for all items in the cart
    return sum(item.quantity * item.product.price for item in cart_items)