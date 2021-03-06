from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    address  = models.CharField(max_length=500)
    cover_pic = models.ImageField(default='cover.jpg', upload_to='cover_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # RESIZING OUR IMAGE TO 300PX
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

