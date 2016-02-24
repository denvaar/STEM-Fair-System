from django import template

register = template.Library()

@register.filter(name='css')
def css(field, css):
    return field.as_widget(attrs={"class":css})

@register.filter(name='placeholder')
def placeholder(value, token):
    value.field.widget.attrs["placeholder"] = token
    return value

@register.filter(name='sort_by')
def sort_by(queryset, order):
    return queryset.order_by(order)
