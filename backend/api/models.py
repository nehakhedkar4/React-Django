from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
import math

class MyUserManager(BaseUserManager):
    # def create_user(self, phone, password=None, password2=None):
    def create_user(self, email=None, phone=None, password=None, password2=None,fname=None,lname=None):
       
        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            fname=fname,
            lname=lname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, phone, password=None):
    def create_superuser(self, email, phone, password=None):
        user = self.create_user(
            email,
            password=password,
            phone=phone,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    email = models.EmailField(max_length=79,blank=True, null=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True, blank=True, null=True) 
    fname = models.CharField(max_length=78)
    lname = models.CharField(max_length=78)

    otp = models.CharField(max_length=6,blank=True, null=True)
    is_verify = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.phone:
            return self.phone
        else:
            return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

