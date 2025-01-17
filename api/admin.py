from django.contrib import admin

# Register your models here.
from .models import CustomUser,Hobby,UserHobby,FriendRequest,Friendship

admin.site.register(Hobby)
admin.site.register(CustomUser)
admin.site.register(UserHobby)
admin.site.register(FriendRequest)
admin.site.register(Friendship)
