from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, first_name, last_name, username, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is Required")

        if not username:
            raise ValueError("Username is Required")

        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, first_name = None, last_name = None, username = None, email = None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(first_name, last_name, username, email, password, **extra_fields)

    def create_superuser(self, first_name = None, last_name = None, username = None, email = None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(first_name, last_name, username, email, password, **extra_fields)

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=11, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_lahel):
        return True