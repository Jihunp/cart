from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

#create new user
#create superuser
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Must have an email address")
        if not username:
            raise ValueError("Must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(make_password(password))
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_admin = True,
            is_staff = True,
            is_superuser = True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=70, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login= models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
