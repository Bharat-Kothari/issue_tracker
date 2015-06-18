from wsgiref.validate import validator
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.db import models

# Create your models here.
class MyUserManager(BaseUserManager):
    # use_in_migrations = True

    def _create_user(self, emailaddr, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """

        if not emailaddr:
            raise ValueError('The given username must be set')

        user = self.model(emailaddr=emailaddr,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, emailaddr, password=None, **extra_fields):
        return self._create_user(emailaddr, password, False, False,
                                 **extra_fields)

    def create_superuser(self, emailaddr, password, **extra_fields):
        return self._create_user(emailaddr, password, True, True,
                                 **extra_fields)


class MyUser(AbstractBaseUser,PermissionsMixin):

    emailaddr = models.EmailField(('emailaddr'), max_length=50, unique=True,
        help_text=('Required. 50 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        error_messages={
            'unique': ("A emailaddr with that already exists."),
        })
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    dob = models.DateField('date of bith', null=True)
    is_staff = models.BooleanField(('staff status'), default=False,
    help_text=('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(('active'), default=True,
        help_text=('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    objects = MyUserManager()

    USERNAME_FIELD = 'emailaddr'





# #class user_table(models.Model)
#
#     emailadd = models.EmailField(max_length=75 ,primary_key=True)
#     password=models.CharField(max_length=30)
#     fname=models.CharField(max_length=50)
#     lname=models.CharField(max_length=50)




# class new_project(models.Model):
#
#     emailadd=models.ForeignKey(user_table)
#     projtitle=models.CharField(max_length=30 ,primary_key=True)
#     description=models.CharField(max_length=500)
#
#
#
# class projects_member(models.Model):
#     projtitle=models.ForeignKey(new_project)
#     emailadd=models.ForeignKey(user_table)



# #class stories(models.Model):
#     projtitle=models.ForeignKey(new_project)
#     emailadd=models.ForeignKey(user_table)
#     storytitle=models.CharField(max_length=50)
#     description=models.CharField(max_length=500)
#     assignee = models.ForeignKey(user_table)
#     estimate=models.IntegerField("in hours")
#     status_choice=(
#         ('strtd','started'),
#         ('finsh','finished'),
#         ('deliv','delivered')
#     )
#     status=models.CharField(max_length=5,choices=status_choice)
#     scheduled_choice=(
#         ('ys','yes'),
#         ('no','no')
#     )
#     scheduled=models.CharField(max_length=2,choices=scheduled_choice)
#     visibilty=models.BooleanField(default=True)
