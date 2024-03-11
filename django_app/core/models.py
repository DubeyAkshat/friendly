from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from .validators import UsernameValidator

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=self.model.normalize_username(username),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username=username, email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UsernameValidator()

    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to="profile_images", default='blank-profile-picture.png')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'date_of_birth']
    
    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser
    
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save()
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('username'),
                name='unique_username_case_insensitive',
            )
        ]


class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_images")
    caption = models.TextField(max_length=100)
    liked_by = models.ManyToManyField(User, blank=True, related_name="liked_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.caption
