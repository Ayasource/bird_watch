from .models import Bird, Entry
from django import forms


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['body', 'bird_count']
