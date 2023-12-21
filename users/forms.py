from django import forms
from django.contrib.auth.models import User

#login form
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# user signup
class SignupForm(forms.ModelForm):

    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='confirm password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')


    # check if password and confirm password are same
    def check_passwords(self):
        # if not raise error
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise forms.ValidationError('Passwords do not match')

        return self.cleaned_data['password_confirm']

