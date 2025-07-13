from django import forms
from .models import UserSession
from .models import Answer

class UploadForm(forms.ModelForm):
    class Meta:
        model = UserSession
        fields = ['name', 'email', 'uploaded_file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'uploaded_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }



class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']  # Replace with actual field(s) from your Answer model
