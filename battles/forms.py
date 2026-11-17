from django import forms

from .models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['team', 'code_snapshot']
        widgets = {
            'code_snapshot': forms.Textarea(attrs={
                'rows': 20,
                'cols': 80,
                'placeholder': 'Вставьте ваш код сюда...',
            }),
        }