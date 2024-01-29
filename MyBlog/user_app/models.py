from django.db import models
from django.contrib.auth.models import User
from post_app.models import Post


class UserAdditional(models.Model):
    linked_user = models.OneToOneField(User, related_name='linked_user', on_delete=models.CASCADE)
    avatar = models.ImageField("avatar", default='static/images/avatars/default.jpg',
                               upload_to='static/images/avatars/')
    birthday = models.DateField("birthday", blank=True, null=True)
    favorite_posts = models.ManyToManyField(Post, related_name='favorite_posts')
    liked_posts = models.ManyToManyField(Post, related_name='liked_posts')

    def __str__(self):
        return self.username

