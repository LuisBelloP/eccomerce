from django import template

register = template.Library ()


@register.filter (name='is_in_cart')
def is_in_cart(product, cart):
    if product is None or cart is None:
        return False
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False


@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    print('estuviste en cart_quantity')
    if not isinstance(product, str) and hasattr(product, 'id'):
        product_id = product.id
    elif isinstance(product, str) and product.isdigit():
        product_id = int(product)
    else:
        return 0
    keys = cart.keys()
    for id in keys:
        if int(id) == product_id:
            return cart.get(id)
    return 0



@register.filter (name='price_total')
def price_total(product, cart):
    return product.price * cart_quantity (product, cart)


@register.filter (name='total_cart_price')
def total_cart_price(products, cart):
    sum = 0
    for p in products:
        sum += price_total (p, cart)

    return sum