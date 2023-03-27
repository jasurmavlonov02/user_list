from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db.models import TextChoices
from django.db.transaction import atomic
from django.forms import ModelForm, CharField, TextInput, EmailField, Form, DateTimeField, DateField, DateInput, \
    ImageField

from users.models import Profile


class ProfileModelForm(ModelForm):
    username = CharField(label='F.I.O')
    phone = CharField(label='Telefon raqami', max_length=9)
    email = EmailField(label="Elektron pochtasi")
    address = CharField(label="Uy manzili")
    position = CharField(label="Lavozimi")
    image = ImageField(label="Rasmi")
    medical_examination_date = DateTimeField(label="Tibbiy ko'rikdan o'tgan sanasi")
    otpusk = DateTimeField(label="Ta'tilga chiqish sanasi")
    #
    zavod_dopusk = ArrayField(CharField(label="Zavodga kirish ruhsatnomasi"), blank=True, default=list)
    birth_day = DateTimeField(label="Tug'ilgan kuni")

    class Meta:
        model = Profile
        birth_day = DateField(
            widget=DateInput(format='%d%m%Y'),
            input_formats=['%d%m%Y']
        )  # Perhaps you should consider a separator in this format i.e. `%d-%m-%Y` instead of `%d%m%Y`
        medical_examination_date = DateField(
            widget=DateInput(format='%d%m%Y'),
            input_formats=['%d%m%Y']
        )
        otpusk = DateField(
            widget=DateInput(format='%d%m%Y'),
            input_formats=['%d%m%Y']
        )
        # fields = (
        #     'username', 'category', 'position', 'birth_day',
        #     'medical_examination_date', 'otpusk',
        #     'email', 'phone', 'address', 'zavod_dopusk',
        #     'image',
        # )
        exclude = ()


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
        user.is_staff = True
        user.is_superuser = True
        user.set_password(self.cleaned_data.get('password'))
        user.save()
