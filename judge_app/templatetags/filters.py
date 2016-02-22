from django import template

register = template.Library()
@register.filter(name='css')
@register.filter(name='placeholder')

def css(field, css):
    return field.as_widget(attrs={"class":css})

def placeholder(value, token):
    value.field.widget.attrs["placeholder"] = token
    return value
