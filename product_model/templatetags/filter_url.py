from django import template
from urllib.parse import urlencode, parse_qs

register = template.Library()

@register.filter
def remove_page(query_string):
    query_dict = parse_qs(query_string)
    query_dict.pop('page', None)  # حذف پارامتر page
    return urlencode(query_dict, doseq=True)
