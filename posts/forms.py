from django import forms
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'placeholder': 'Invade some timelines...','maxlength': '120',}))
    class Meta:
        model = Post
        fields = ('content', 'image')

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a coment...'}))
    class Meta:
        model = Comment
        fields = ('body',)