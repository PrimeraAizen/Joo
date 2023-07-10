from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Courses(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    author = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    published = models.BooleanField(default=False)
    last_viewed = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    bio = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class PublishRequest(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ' - ' + self.course.title

    class Meta:
        verbose_name = 'Publish Request'
        verbose_name_plural = 'Publish Requests'