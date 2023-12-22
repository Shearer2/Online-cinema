from django import forms
from movies.models import Reviews, Rating, RatingStar, Contact


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')


# Форма для показа рейтинга фильма.
class RatingForm(forms.ModelForm):
    # При помощи queryset забираем все созданные звёзды, widget - это то, как будет представлена форма в html.
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('star',)


class ContactForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'editContent', 'placeholder': 'Enter your email...'
    }))

    class Meta:
        model = Contact
        fields = ('email',)
        # Убираем label.
        labels = {
            'email': ''
        }
