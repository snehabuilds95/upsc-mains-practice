


from django import forms
from .models import UserSession, Answer

class UploadForm(forms.ModelForm):
    class Meta:
        model = UserSession
        fields = ['name', 'email', 'uploaded_file']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 6})
        }
