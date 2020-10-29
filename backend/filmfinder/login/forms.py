from django import forms


class UserForm(forms.Form):
    name = forms.CharField(label='name', max_length=50)
    password = forms.CharField(label='password', max_length=20)

