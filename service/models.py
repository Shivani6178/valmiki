from django.db import models
from django.utils import timezone

class GeneratedBlog(models.Model):
    blog_title = models.CharField(max_length=100, blank=False, null=False)
    blog_content = models.CharField(max_length=100, blank=True, null=True)
    blog_type = models.CharField(max_length=100, blank=False, null=False, default="Professional")
    reward = models.BooleanField(default=False)
    created_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = timezone.now()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.blog_title

class UserQuery(models.Model):
    user_email = models.CharField(max_length=100, blank=False, null=False)
    user_query = models.CharField(max_length=500, blank=False, null=False)
    created_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user_email