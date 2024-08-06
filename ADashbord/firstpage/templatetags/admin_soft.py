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
