from django import template


register = template.Library()


@register.filter
def format_selftext(value, arg):
    if value:
        filter = int(arg)
        words = value.split()

        value = f'{" ".join(words[:filter])} ...'

    return value

