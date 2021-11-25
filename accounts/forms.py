from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import User
from django import forms


class CustomUserChangeForm(UserChangeForm):
    password = None
    nickname = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nickname',
                'id': 'floatingNickname',
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ('nickname', 'profile_image',)


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)

        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None

        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
            'id': 'floatingOldPassword',
            'placeholder': 'example',
        })
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingNewPassword1',
            'placeholder': 'example',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingNewPassword2',
            'placeholder': 'example',
        })


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['username'].label = '아이디'
        self.fields['username'].widget.attrs.update({     
            'class': 'form-control',
            'autofocus': False,
            'id': 'floatingInput',
            'placeholder': 'example',
        })
        self.fields['nickname'].label = '닉네임'
        self.fields['nickname'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingNickname',
            'placeholder': 'Nickname',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingEmail',
            'placeholder': 'Email',
        })
        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingPassword1',
            'placeholder': 'example',
        })
        self.fields['password2'].label = '비밀번호 확인'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingPassword2',
            'placeholder': 'example',
        })

    class Meta:
        model = User
        fields = ['username', 'nickname', 'email', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
            'id': 'floatingInput',
            'placeholder': 'example',
        })
        self.fields['password'].label = '비밀번호'
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingPassword',
            'placeholder': 'Password',
        })

