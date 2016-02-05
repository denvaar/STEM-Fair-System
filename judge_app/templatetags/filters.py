from django import template

register = template.Library()
@register.filter(name='css')

def css(field, css):
    return field.as_widget(attrs={"class":css})
