import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class Guideline(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Compliance Guideline'
        verbose_name_plural = 'Compliance Guidelines'


def unique_file_name(instance, filename):
    """
    Generates a unique filename for the given instance and filename.
    Args:
        instance: The instance of the model.
        filename: The original filename.
    Returns:
        A string representing the unique filename.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('uploads/', filename)


class Content(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=unique_file_name)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content')
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (v-{self.version})"

    @property
    def review_status(self):
        try:
            passed_reviews = self.review_items.filter(
                status=ReviewItem.StatusChoices.PASSED
            ).count()
            if passed_reviews == self.review_items.count():
                return "Completed"
            else:
                return "Pending"
        except ObjectDoesNotExist:
            return "No review items"


class ReviewItem(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PASSED = 'PASS', 'Passed'
        FAILED = 'FAIL', 'Failed'

    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name='review_items'
    )
    guideline = models.ForeignKey(Guideline, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='review_items',
    )
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.guideline} - {self.status}"
