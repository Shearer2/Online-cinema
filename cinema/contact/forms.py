from django import forms
from contact.models import Contact


class ContactForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'type': 'email', 'class': 'editContent', 'placeholder': 'Enter your email...'
    }))

    class Meta:
        model = Contact
        fields = ('email',)
        # Убираем label.
        labels = {
            'email': ''
        }

