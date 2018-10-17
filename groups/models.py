from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, default='')
    slug = models.SlugField(allow_unicode=True, unique=True)
    created_date = models.DateTimeField(default=timezone.now())
    leader = models.ForeignKey(User, related_name='leader', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through='Membership')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("groups:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField()

    def __str__(self):
        return self.user.username
