from .models import Bird
from django import forms


class EntryForm(forms.ModelForm):
    class Meta:
        model = Bird
        fields = ['bird_name', 'bird_count']
