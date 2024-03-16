from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    display_name = models.CharField(max_length=15)
    user_id = models.CharField(max_length=255, unique=True)
    bio = models.CharField(max_length=240, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, blank=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='user_set_custom',
        related_query_name='user_custom',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='user_set_custom',
        related_query_name='user_custom'
    )

    def __str__(self):
        return self.username


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    media = models.ImageField(upload_to='post_media', blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content}'

    def get_like_count(self):
        return self.like_set.count()

    def get_retweet_count(self):
        return self.retweet_set.count()

    def get_replies_count(self):
        return self.comment_set.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'tweet']

    def __str__(self):
        return f'{self.user.username} likes {self.tweet}'


class Retweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'tweet']

    def __str__(self):
        return f'{self.user.username} retweets {self.tweet}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.tweet}'
