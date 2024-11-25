from django import forms
from .models import Comments

class CommentsForm(forms.ModelForm):
    upload = forms.FileField(label='첨부 파일', required=False, 
          widget=forms.FileInput(attrs={'class': 'form'}))
    
    class Meta:
        model = Comments
        exclude = ['attached']