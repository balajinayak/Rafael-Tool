from django import template

register = template.Library()

@register.filter
def remove_duplicates(data):
    return list(set(data))



@register.filter(name='first_word')
def first_word(value):
    words = value.split(".")
    if words:
        return words[0]
    return ''