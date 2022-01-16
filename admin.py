from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Profile, FriendRequest, BlockFriend , MessageFriend

admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(BlockFriend)
admin.site.register(MessageFriend)
