from django import forms
from .models import Review


class ReviewTextForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
