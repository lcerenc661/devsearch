from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver 

from .models import *
from django.contrib.auth.models import User

from django.core.mail  import send_mail
from django.conf import settings

#@receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    print('Profile signal triggered')
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user, 
            username=user.username,
            email=user.email,
            name=user.first_name,
        )  
        subject = 'Welcome to Devsearch'
        message = 'We are glad you are here'
        send_mail(
            subject,
            message, 
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
         )
        
        
              
def updateUser(sender, instance, created, **kwrgas):
    profile =  instance
    user = profile.user
    
    if created ==False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
    

#@receiver(post_delete, sender=Profile)    
def deleteUSer(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
    
    
    
post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUSer, sender=Profile)