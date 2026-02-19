from django import template

register=template.Library()

@register.filter()
def multiply(value,count):
    try:
        return int(value) * int(count)
    except(ValueError,TypeError):
        return 0
