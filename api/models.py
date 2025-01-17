from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
    

class Hobby(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    def as_dict(self):
        return {"id":self.id, 
                "name":self.name, 
                ## add reverse api later "api":reverse("hobby_detail", args=[self.id])
                }

class UserHobby(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hobby')  # Prevent duplicates

    def __str__(self):
        return f"{self.user.username} - {self.hobby.name}"
    
    def as_dict(self):
        return {"id":self.id, 
                "user": self.user.as_dict(),
                "hobby":self.hobby.as_dict(),
                "date_added":self.date_added,
                ## add reverse api later "api":reverse("book_detail", args=[self.id])
                }

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, through='UserHobby', related_name="users")
    friends =  models.ManyToManyField('CustomUser', through='Friendship', blank=True)

    def as_dict(self):
        return {"id":self.id, 
                "name":self.name, 
                "username":self.username,
                "email":self.email, 
                "date_of_birth":self.date_of_birth, 
                "hobbies":[[hobby.id, hobby.name] for hobby in self.hobbies.all()],
                "isstaff":self.is_staff
                ## add reverse api later "api":reverse("book_detail", args=[self.id])
                }
    
    def as_dict_current_user(self): # FIX THIS USER OR USERNAME???
        return {"id":self.id, 
                "name":self.name, 
                "username":self.username,
                "email":self.email, 
                "date_of_birth":self.date_of_birth, 
                "hobbies":[[hobby.id, hobby.name] for hobby in self.hobbies.all()],
                "password":self.password,
                ## add reverse api later "api":reverse("book_detail", args=[self.id])
                }
    
    ##model to track friend requests    
class FriendRequest(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="receiver", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('sender', 'receiver')  # Prevent duplicate friend requests

    def __str__(self):
        return f"Friend request from {self.sender} to {self.receiver}"
    
    def as_dict(self):
        return{ "id":self.id,
                "sender":self.sender.as_dict(),
                "receiver":self.receiver.as_dict(),
                }

##model to track friendships
class Friendship(models.Model):
    user1 = models.ForeignKey(CustomUser, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(CustomUser, related_name='user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')  # Prevent duplicate friendships

    def __str__(self):
        return f"{self.user1} is friends with {self.user2}"
    
    def as_dict(self):
        return{ "id":self.id,
                "user1":self.user1.as_dict(),
                "user2":self.user2.as_dict(),
                }