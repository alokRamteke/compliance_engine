from django.db import models
from django.contrib.auth.models import User


class Guideline(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


class Content(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    version = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)


class ReviewItem(models.Model):
    class StatusChoices(models.TextChoices):
        PASSED = 'PASS', 'Passed'
        FAILED = 'FAIL', 'Failed'

    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    guideline = models.ForeignKey(Guideline, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=StatusChoices.choices)
