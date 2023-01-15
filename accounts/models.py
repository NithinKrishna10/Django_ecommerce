from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import datetime
# from datetime import datetime

current_date = datetime.date.today()


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50,unique=True)

    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    is_superadmin    = models.BooleanField(default=False)
    signup_day = models.CharField(max_length = 50,default=current_date.day)
    signup_month = models.CharField(max_length = 50,default=current_date.month)
    signup_year = models.CharField(max_length = 50,default=current_date.year)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    email           = models.EmailField(max_length=100,default=1)
    phone_number    = models.CharField(max_length=50,default=1)

    def __str__(self):
        return self.user.first_name

   

class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    phone1 = models.CharField(max_length=15,default=0)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=255)
    phone2 = models.CharField(max_length=15,default=0)
    
    def __str__(self):
        return self.user.first_name


class Return_request(models.Model):
    user = models.ForeignKey(Account,on_delete = models.CASCADE)
    order_number = models.CharField(max_length=15,default=1)
    reason = models.CharField(max_length = 500)
    
