from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class MyAccountManager(BaseUserManager):
    # ---START Creation of normal user operation---
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Must have an email address.')
        if not username:
            raise ValueError('Must have a username.')
        user = self.model(
            # Normalize email changes uppercases in email entry to lowercase.
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    # ---END Creation of normal user operation---
    # ---START Creation of SUPER user operation---
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user
    # ---END Creation of SUPER user operation---

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=50)
    profile_pic = models.ImageField(blank=True)

    # required:
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Here, we are telling the Account class that we are using all of the operations from the MyAccountManager class to create users.
    objects = MyAccountManager()

    # When we return the Account object inside our template this should return the email address.
    def __str__(self):
        return self.email

    # Returns True if the user has the named permission. If obj is provided, the permission needs to be checked against a specific object instance.
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Returns True if the user has permission to access models in the given app. 
    def has_module_perms(self, add_label):
        return True
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class UserProfile(models.Model):
    # One to one is unique because you can only have one account to one userprofile, unlike previous foreign key fields where there could be multiple instances of a relationship
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.user.email

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def full_user_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    