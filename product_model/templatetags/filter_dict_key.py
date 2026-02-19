from django import template

register = template.Library()

@register.filter
def dict_key(dictionary, key):
    """
    دریافت مقدار از دیکشنری با استفاده از کلید
    """
    return dictionary.get(key, 0)  # اگر کلید وجود نداشت، ۰ برمی‌گرداند
