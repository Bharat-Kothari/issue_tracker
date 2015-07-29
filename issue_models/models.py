from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

from datetime import datetime


class MyUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """

        if not email:
            raise ValueError('The given username must be set')

        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(('email'), max_length=50, unique=True,
        help_text=('Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': ("A email with that already exists."),
        })
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=30)
    dob = models.DateField('date of birth', null=True)
    photo = models.ImageField(blank=True, upload_to='images')
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
        # Returns the short name for the user.
        return self.first_name

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


# Model for project
class Project(models.Model):

    project_manager = models.ForeignKey(MyUser, related_name='Manager')
    project_title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    assigned_to = models.ManyToManyField(MyUser)

    def __unicode__(self):
        return self.project_title


# model for story of projects
class Story(models.Model):

    project_title = models.ForeignKey(Project)
    email = models.ForeignKey(MyUser, related_name='Story_Creator')
    story_title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    assignee = models.ForeignKey(MyUser, blank=True, null=True)
    estimate = models.PositiveIntegerField(default=0)
    date = models.DateField(default=datetime.now)
    unstrtd = 'unstrtd'
    strtd = 'strtd'
    finish = 'finish'
    deliv = 'deliv'
    status_choice = (
        (unstrtd, 'notstarted'),
        (strtd, 'started'),
        (finish, 'finished'),
        (deliv, 'delivered')
    )
    status = models.CharField(max_length=7, choices=status_choice, default=unstrtd)
    ys = 'ys'
    no = 'no'
    scheduled_choice = (
        (ys, 'yes'),
        (no, 'no')
    )
    scheduled = models.CharField(max_length=2, choices=scheduled_choice, default='no')
    visibility = models.BooleanField(default=True)

    def __unicode__(self):
        return self.story_title