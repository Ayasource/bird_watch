from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"))


class Bird(models.Model):
    bird_name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=200, unique=False, default='')
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    bird_count = models.PositiveIntegerField(unique=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.created_by} saw {self.bird_count} {self.bird_name}(s) on {self.date.strftime('%Y-%m-%d')}"


class Entry(models.Model):
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE, related_name="entries")
    body = models.TextField()
    bird_count = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.created_by} entry on {self.bird.bird_name}"
