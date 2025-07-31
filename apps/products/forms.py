from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'rating', 'title', 'comment', 'owned_duration',
            'recommend', 'pros', 'cons'
        ]
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]),
            'title': forms.TextInput(attrs={
                'class': 'form-control-custom',
                'placeholder': 'Summarize your review in one line',
                'required': True
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control-custom',
                'rows': 6,
                'placeholder': 'Share your experience with this product...',
                'required': True
            }),
            'owned_duration': forms.Select(attrs={'class': 'form-control-custom'}),
            'recommend': forms.Select(attrs={'class': 'form-control-custom', 'required': True}),
            'pros': forms.Textarea(attrs={
                'class': 'form-control-custom',
                'rows': 3,
                'placeholder': 'List the best features...'
            }),
            'cons': forms.Textarea(attrs={
                'class': 'form-control-custom',
                'rows': 3,
                'placeholder': 'Any areas for improvement...'
            }),
        }