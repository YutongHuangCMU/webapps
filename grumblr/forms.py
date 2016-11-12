from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from grumblr.models import *


class RegistrationForm(forms.Form):

    username1 = forms.CharField(max_length=30,
                               label='Username',
                               widget=forms.TextInput(attrs={'placeholder':"Username", 'class':"form-control"}))
    first_name = forms.CharField(max_length=30,
                                 label='First name',
                                  widget=forms.TextInput(attrs={'placeholder':"First name", 'class':"form-control"}))
    last_name = forms.CharField(label='Last name',
                                widget=forms.TextInput(attrs={'placeholder':"Last name", 'class':"form-control"}))
    email_add = forms.EmailField(label='Email address',
                                widget=forms.TextInput(attrs={'placeholder':"Email address", 'class':"form-control"}))
    email_con = forms.EmailField(max_length=100,
                                label='Email confirmation',
                                widget=forms.TextInput(attrs={'placeholder':"Email confirmation", 'class':"form-control"}))
    password = forms.CharField(max_length=200,
                               label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':"form-control"}))
    password_con = forms.CharField(max_length=200,
                                   label='Confirm password',
                                   widget=forms.PasswordInput(attrs={'placeholder':'Confirm password', 'class':"form-control"}))

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        #print(cleaned_data)
        username = cleaned_data.get('username1')
        password = cleaned_data.get('password')
        password_con = cleaned_data.get('password_con')
        if password and password_con and password != password_con:
            raise forms.ValidationError("Passwords did not match.")

        username1 = self.cleaned_data.get('username1')
        # raise forms.ValidationError("Username is already taken." + str(username1))
        # if User.objects.filter(username__exact=username1):
        #     raise forms.ValidationError("Username is already taken.")
        return cleaned_data

    def clean_username1(self):
        username1 = self.cleaned_data.get('username1')
        #raise forms.ValidationError("Username is already taken.")
        if User.objects.filter(username=username1):
            raise forms.ValidationError("Username is already taken.")
        return username1

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30,
                               label='Username',
                               widget=forms.TextInput(attrs={'placeholder':"Username", 'class':"form-control"}))
    password = password = forms.CharField(max_length=200,
                               label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':"form-control"}))

class PostForm(forms.Form):
    post = forms.CharField(max_length=42,
                               label='post',
                               widget=forms.TextInput(attrs={'id':"txt-post", 'placeholder':"What is in your mind?", 'class':"form-control"}))
    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        #print(cleaned_data)
        post = cleaned_data.get('post')
        if len(post) == 0:
            raise forms.ValidationError("The post cannot be empty!")
        if len(post) > 42:
            raise forms.ValidationError("The post cannot be longer than 42 characters!")
        return cleaned_data

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=42,
                               label='comment',
                               widget=forms.TextInput(attrs={'id':"txt-com", 'placeholder':"Add comment here...", 'class':"input-com"}))

                               
    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        #print(cleaned_data)
        comment = cleaned_data.get('comment')
        if len(post) == 0:
            raise forms.ValidationError("The comment cannot be empty!")
        if len(post) > 42:
            raise forms.ValidationError("The post cannot be longer than 42 characters!")
        return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','followings','token_password')
        widgets = {'photo': forms.ClearableFileInput(),
                   'first_name': forms.TextInput(attrs={'placeholder':"First name", 'class':"form-control"}),
                   'last_name': forms.TextInput(attrs={'placeholder':"Last name", 'class':"form-control"}),
                   'age': forms.NumberInput(attrs={'placeholder':"Age", 'class':"form-control"}),
                   'short_bio': forms.Textarea(attrs={'placeholder':"Short bio", 'class':"form-control"})}

class ForgetForm(forms.Form):
    username = forms.CharField(max_length = 200,
                               label = 'Username',
                               widget=forms.TextInput(attrs={'placeholder':'Username', 'class':"form-control"}))
    def clean(self):
        cleaned_data = super(ForgetForm, self).clean()
        username1 = cleaned_data.get('username')
        if not User.objects.filter(username__exact=username1):
            raise forms.ValidationError("Username does not exist!")
        return cleaned_data

class PasswordForm(forms.Form):
    password1 = forms.CharField(max_length = 200,
                               label = 'New password',
                               widget=forms.PasswordInput(attrs={'placeholder':'New password', 'class':"form-control"}))
    password2 = forms.CharField(max_length = 200,
                               label = 'Confirm new password',
                               widget=forms.PasswordInput(attrs={'placeholder':'Confirm new password', 'class':"form-control"}))

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data
