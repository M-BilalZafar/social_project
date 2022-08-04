from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model



#my imorts

import uuid
from datetime import datetime
# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    first_name=models.CharField( max_length=50)
    last_name=models.CharField( max_length=50)
    id_user = models.IntegerField()
    bio =  models.TextField(blank=True)
    location = models.CharField( max_length=50 ,  blank=True)
    profile_img=models.ImageField( upload_to='profile_image', default="default_profile.jpg")
    
    
    
    
    def __str__(self):
        return self.user.username
    
    
    
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user= models.CharField( max_length=50)
    image = models.ImageField(upload_to="post", height_field=None, width_field=None, max_length=None)
    caption= models.TextField()
    created_at= models.DateTimeField(default=datetime.now)
    no_of_likes=    models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.user
    
    
class LikePost(models.Model):
    post_id=models.CharField( max_length=100)    
    username=models.CharField( max_length=100)    
    
    def __str__(self):
        return self.username
    
    
    
class FollowersCount(models.Model):
    follower = models.CharField( max_length=1000)
    user = models.CharField( max_length=100)
    
    
    
    def __str__(self):
        return self.user
     