from django import template

register = template.Library()


@register.filter(is_safe=True)
def remove_others(text):
    result = [line for line in text.splitlines() if 'other' not in line]
    return "\n".join(result)
