from django import forms
from contact.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('email',)
        # Добавляем плейсхолдер к нашему полю для отображения необходимого текста в самом поле.
        widgets = {
            'email': forms.TextInput(attrs={'class': 'editContent', 'placeholder': 'Your Email...'})
        }
        # Убираем label.
        labels = {
            'email': ''
        }

