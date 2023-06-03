from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import MyUser, MyUserManager


class UserCreationForm(forms.ModelForm):
    # 사용자 생성 폼
    email = forms.EmailField(
        label=_('email'),
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('email address'),
                'required': 'True',
            }
        )
    )
    username = forms.CharField(
        label=_('user name'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('user name'),
                'required': 'True',
            }
        )
    )
    mobile = forms.CharField(
        label=_('mobile phone number'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('mobile phone number'),
                'required': 'True',
            }
        )
    )
    password1 = forms.CharField(
        label=_('password'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('password'),
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label=_('password confirmation'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('password confirmation'),
                'required': 'True',
            }
        )
    )

    class Meta:
        model = MyUser
        fields = ('email', 'username', 'mobile')

    def clean_password2(self):
        # 두 비밀번호 입력 일치 확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.email = MyUserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    # 비밀번호 변경 폼
    password = ReadOnlyPasswordHashField(
        label=_('password')
    )

    class Meta:
        model = MyUser
        fields = ('email', 'username', 'mobile', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]