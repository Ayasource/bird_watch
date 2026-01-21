from .models import Bird
from django import forms


class BirdForm(forms.ModelForm):
    class Meta:
        model = Bird
        fields = ['bird_name', 'bird_count', 'status']
        widgets = {
            'status': forms.Select(choices=[(1, 'Published')])
        }
