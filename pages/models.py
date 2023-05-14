from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=250)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page-detail', kwargs={'pk':self.pk})

class Comments(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=50)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=False)

    class Meta:
        ordering=['-created','-updated']

    def __str__(self):
        return 'comment {} by {} '.format(self.body,self.name)
  