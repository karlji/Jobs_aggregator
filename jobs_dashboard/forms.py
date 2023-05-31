from django import forms
from .models import JudgeDetail

class JudgesForm(forms.ModelForm):
    class Meta:
        model = JudgeDetail #Model only used to creat form fields atm
        fields = '__all__'
        widgets = {
        'password': forms.PasswordInput(),
        
    }