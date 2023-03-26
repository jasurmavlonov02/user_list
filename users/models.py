from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import integer_validator
from django.db.models import CharField, EmailField, ImageField, DateTimeField, TextChoices, Model, SlugField, \
    ForeignKey, CASCADE
from django.utils.text import slugify


# Create your models here.


class Profile(Model):
    class ZavodChoice(TextChoices):
        NMZ = 'NMZ'
        GMZ = 'GMZ'
        SHMZ = 'SHMZ'

    username = CharField(max_length=100, unique=False)
    phone = CharField(max_length=9, validators=[integer_validator])
    email = EmailField(unique=True)
    address = CharField(max_length=255)
    position = CharField(max_length=100)
    image = ImageField(upload_to='images/')
    medical_examination_date = DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    otpusk = DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    category = ForeignKey('Category', CASCADE, null=True, blank=True)

    zavod_dopusk = CharField(max_length=25, choices=ZavodChoice.choices)
    birth_day = DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    class Meta:
        ordering = ('-id',)


class Category(Model):
    name = CharField(max_length=100)
    slug = SlugField(unique=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = slugify(self.name)
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f'{self.slug} - 1'
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


#akmal