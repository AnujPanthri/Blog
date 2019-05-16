from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(blank=True, null=True, upload_to='profile/')
    url = models.URLField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    def __str__(self):
        return "user profile of {}".format(self.user.username)

def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
post_save.connect(create_user_profile, User)