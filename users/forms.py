from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, TextInput, EmailField

from users.models import Profile


class ProfileModelForm(ModelForm):
    birth_day = CharField(widget=TextInput(attrs={'type': 'date'}))
    medical_examination_date = CharField(widget=TextInput(attrs={'type': 'date'}))
    otpusk = CharField(widget=TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = (
            'username', 'category', 'position', 'birth_day',
            'medical_examination_date', 'otpusk',
            'email', 'phone', 'address', 'zavod_dopusk',
            'image',
        )


class LoginForm(AuthenticationForm):
    email = EmailField(required=False)
    password = CharField(max_length=255)
    username = CharField(required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise ValidationError('Bunday username yo\'q')
        return username

    def clean_password(self):
        username = self.data.get('username')
        password = self.data.get('password')

        user = User.objects.filter(username=username).first()

        if not user.check_password(password):
            raise ValidationError('Parol xato')

        return password

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
