from django import template

register=template.Library()

@register.filter()
def price_view(price):
    price_with_dot=[]
    st_price=str(price)
    st_price=st_price[::-1]
    for i in range(len(st_price)):
        if i == 3 or i ==6 or i ==9 or i ==12 or i ==15 or i ==18:
            price_with_dot.append(',')
        price_with_dot.append(st_price[i])
    price_with_dot=price_with_dot[::-1]
    result="".join(price_with_dot)
    return result


