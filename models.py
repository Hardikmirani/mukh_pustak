from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings
from autoslug import AutoSlugField

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='abc1.png', upload_to = 'profile_pic')
	slug = AutoSlugField(populate_from='user')
	bio = models.CharField(max_length=255, blank=True)
	friends = models.ManyToManyField("Profile", blank=True)
	onoff = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user.username)

	def get_absolute_url(self):
		return "/users/{}".format(self.slug)

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)

class FriendRequest(models.Model):
	to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
	from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "From {}, to {}".format(self.from_user.username, self.to_user.username)

class BlockFriend(models.Model):
	b_to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='b_to_user', on_delete=models.CASCADE)
	b_from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='b_from_user', on_delete=models.CASCADE)

	def __str__(self):
		return "From {}, to {}".format(self.b_from_user.username, self.b_to_user.username)


class MessageFriend(models.Model):
	m_to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='m_to_user', on_delete=models.CASCADE)
	m_from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='m_from_user', on_delete=models.CASCADE)
	message =  models.CharField(max_length=255, blank=True)
	timestamp =  models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "From {}, to {}".format(self.m_from_user.username, self.m_to_user.username)

