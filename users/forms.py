from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Userdata

class CustomUserForm(UserCreationForm):
    country = forms.CharField(max_length=100, required=False)
    address = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=30, required=False)
    state = forms.CharField(max_length=30, required=False)
    zip_code = forms.CharField(max_length=10, required=False)
    phone_no = forms.CharField(max_length=18, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "username", "email", "first_name", "last_name", "password1", "password2",
            "country", "address", "city", "state", "zip_code", "phone_no", "profile_picture"
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        userdata, created = Userdata.objects.update_or_create(
            user=user,
            defaults={
                'country': self.cleaned_data.get('country'),
                'address': self.cleaned_data.get('address'),
                'city': self.cleaned_data.get('city'),
                'state': self.cleaned_data.get('state'),
                'zip_code': self.cleaned_data.get('zip_code'),
                'phone_no': self.cleaned_data.get('phone_no'),
                'profile_picture': self.files.get('profile_picture')
            }
        )
        return user
