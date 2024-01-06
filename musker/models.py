from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followed_by', blank=True)
    date_modified = models.DateTimeField(User ,auto_now = True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='pro_images')

    def __str__(self):
        return self.user.username
    
    def save(self):
        super().save()

        img = Image.open(self.profile_image.path)
        if img.height > 300 and img.width > 300:
            new_size = (300, 300)
            img.thumbnail(new_size)
            img.save(self.profile_image.path)

    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


# post_save.connect(create_profile, sender=User)


class Tweet(models.Model):
    user = models.ForeignKey(User, related_name='tweest', on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='tweet_likes', blank=True)


    def number_of_likes(self):
        return self.likes.count()


    def __str__(self):
        return (
            f'{self.user} '
            f'{self.created: %Y/%m/%d-(%H:%M)} '
            f'{self.body}...'
        )