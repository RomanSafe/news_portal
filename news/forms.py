from django import forms

class NewPostForm(forms.Form):
    title = forms.CharField(label="Title:")
    text = forms.CharField(label="New's text:", widget=forms.Textarea)

class SearchForm(forms.Form):
    q = forms.CharField(label="Search:", required=False)
