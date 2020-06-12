from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True


    def create_user(self, email, name, age, sex, password): #**extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not name:
            raise ValueError("name is needed")
        if not age:
            raise ValueError("age is needed")
        if sex not in [0,1]:
            raise ValueError("sex is needed")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            age=age,
            sex=sex,            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, age, sex, password):# **extra_fields):
        user = self.create_user(
            email = email,
            name='admin',
            age=age,
            sex=sex,
            password=password,            
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email', unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField() # 나이
    sex = models.IntegerField() # 남 0 여 1

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','age','sex']

    objects = UserManager()
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin