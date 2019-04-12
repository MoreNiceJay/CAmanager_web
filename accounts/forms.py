from django import forms
import pycountry
from .models import User


class User(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email',)