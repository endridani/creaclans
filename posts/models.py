from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from groups.models import Group

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)
    group = models.ForeignKey(Group, related_name="posts", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("groups:detail", kwargs={"slug": self.group.slug})

    class Meta:
        ordering = ["-created_date"]


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField
    created_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.text

