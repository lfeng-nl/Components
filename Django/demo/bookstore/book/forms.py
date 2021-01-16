from django import forms

class CommentForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField(required=False)
    content = forms.CharField(widget=forms.Textarea)