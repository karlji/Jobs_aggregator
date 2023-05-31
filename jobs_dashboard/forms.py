from django import forms
from .models import JudgeDetail

class JudgesForm(forms.ModelForm):
    class Meta:
        model = JudgeDetail
        fields = '__all__'
        widgets = {
        'password': forms.PasswordInput(),
        
    }