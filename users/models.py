from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email 								 = models.EmailField(_('email'), unique=True)
    mobile 								 = models.CharField(_('mobile'), max_length=20, unique=True)
    full_name 							 = models.CharField(_('name'), max_length=50, blank=True)
    reset_token                          = models.CharField(_('reset_token'), max_length=50, blank=True, null=True)
    ref 								 = models.CharField(_('ref'), max_length=20, null=True, blank=True)
    date_joined 						 = models.DateTimeField(_('joined_at'), auto_now_add=True)
    is_active 							 = models.BooleanField(_('active'), default=True)
    avatar 								 = models.ImageField(upload_to='avatars/', null=True, blank=True)
    avatar_v2                            = models.CharField(_('avatar_v2'), max_length=500, blank=True)
    status 								 = models.IntegerField(_('status'), default=0, null=True, blank=True) #0 not validate yet , 1 completed, 2 missing/wrong/rejected item
    # current_location                     = models.CharField(_('current_location'), max_length=50, blank=True, null=True)
    objects 							 = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = self.full_name
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.full_name.split(' ')[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=50,blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255,blank=True, null=True)
    country = models.CharField(max_length=50,blank=True, null=True)
    city = models.CharField(max_length=50,blank=True, null=True)
    poscode = models.CharField(max_length=5,blank=True, null=True)
    photo = models.ImageField(upload_to='uploads', blank=True, null=True)