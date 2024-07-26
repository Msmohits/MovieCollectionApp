from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
import pytz

# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True, auto_now=True)
    date_joined = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Movie(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.CharField(max_length=255)
    movie_id = models.UUIDField(blank=False)


class Collection(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    movies = models.ManyToManyField(Movie)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "title"], name="unique_user_title")
        ]
