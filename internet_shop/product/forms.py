from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Order, NewsletterSubscription


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'email', 'address', 'postal_code', 'city']


class NewsletterSubscriptionForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = NewsletterSubscription
        fields = ('email',)