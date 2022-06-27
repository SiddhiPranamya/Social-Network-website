from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user") #user who created the post
    post = models.CharField(max_length=200) # text of the post 
    timestamp = models.DateTimeField() # time stamp of the post
    

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following") # user following
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower") # user with follower
    
