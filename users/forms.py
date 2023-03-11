from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.forms import ModelForm, CharField, TextInput, EmailField, Form

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
        username = self.data.get('username')
        if not User.objects.filter(username=username).exists():
            raise ValidationError('Bunday username yo\'q')
        return username

    def clean_password(self):
        username = self.data.get('username')
        password = self.data.get('password')

        user = User.objects.filter(username=username).first()

        if user and not user.check_password(password):
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


class RegisterForm(Form):
    username = CharField(max_length=255)
    email = EmailField()
    password = CharField(max_length=255)
    confirm_password = CharField(max_length=255)

    def clean_email(self):
        email = self.data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(f' {email} this email is already registered ')
        return email

    def clean_username(self):
        username = self.data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(f' User {username} is already registered ')
        return username

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Comfirm password is not same')
        return password

    @atomic
    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email')
        )
        user.set_password(self.cleaned_data.get('password'))
        user.save()
