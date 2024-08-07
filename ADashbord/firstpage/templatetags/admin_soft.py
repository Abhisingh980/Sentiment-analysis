from django import template

register = template.Library()


@register.simple_tag
def my_custom_tag():
    return 'Hello from my custom tag!'

@register.simple_tag
def get_direction():
    return 'ltr'

@register.simple_tag
def get_admin_setting():
    return 'admin_soft'

@register.simple_tag
def admin_get_menu():
    return 'admin_menu'

@register.filter
def clean_text(value):

    return value.strip()

@register.filter(name='add_class')
def add_class(value, css_class):
    """Add a CSS class to a form field widget."""
    return value.as_widget(attrs={"class": css_class})
