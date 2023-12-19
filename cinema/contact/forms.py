from django import forms
from contact.models import Contact


class ContactForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'type': 'email', 'class': 'editContent', 'placeholder': 'Enter your email...'
    }))

    class Meta:
        model = Contact
        fields = ('email',)
        # Добавляем плейсхолдер к нашему полю для отображения необходимого текста в самом поле.
        #widgets = {
        #    'email': forms.TextInput(attrs={'class': 'editContent', 'placeholder': 'Your Email...'})
        #}
        # Убираем label.
        labels = {
            'email': ''
        }

