from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .manager import UserManager

class User(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    timestamp = models.DateTimeField(_('date joined'), auto_now_add=True)
    staff = models.BooleanField(_('staff status'),default=False)
    admin = models.BooleanField(_('admin status'),default=False)
    active = models.BooleanField(_('active'), default=True)
    #avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()
    def __str__(self):
        return self.first_name

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active

class Farm(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    location = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    topic = models.CharField(max_length=255)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

    class Meta:
           ordering = ('timestamp',)

class Forum(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    message = models.TextField()
    message_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
           ordering = ('timestamp',)
