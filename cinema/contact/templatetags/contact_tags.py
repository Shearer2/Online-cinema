from django import template
from contact.forms import ContactForm

register = template.Library()


# Создаём template tag и возвращаем нашу контактную форму. Регистрируем данный тег как inclusion и указываем путь
# в котором будет находиться шаблон.
@register.inclusion_tag('contact/tags/form.html')
def contact_form():
    return {'contact_form': ContactForm()}

