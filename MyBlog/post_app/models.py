from django.db import models
from django.contrib.auth.models import User

comment_rating_choices = (
    (1, '⭐️'), (2, '⭐️⭐️'), (3, '⭐️⭐️⭐️'), (4, '⭐️⭐️⭐️⭐️'), (5, '⭐️⭐️⭐️⭐️⭐️')
)


class Tag(models.Model):
    tag = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.tag


class Post(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    image = models.ImageField(upload_to='static/images/post_pics/', blank=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    url_name = models.CharField(max_length=225)

    def __str__(self):
        return f'{self.title} ({self.author})'


class Comment(models.Model):
    comment = models.TextField()
    rating = models.IntegerField(default=5, choices=comment_rating_choices)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post}\n{self.comment}\n{self.rating}\n{self.author}'
