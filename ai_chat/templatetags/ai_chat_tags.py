from django import template
from django.utils.safestring import mark_safe

import markdown
import nh3


register = template.Library()


@register.filter
def safe_markdown(value):
    md = markdown.markdown(value)
    sanitized = nh3.clean(md)
    return mark_safe(sanitized)
