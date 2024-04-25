from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Content, Guideline, ReviewItem


@receiver(post_save, sender=Content)
def create_review(sender, instance, created, **kwargs):
    if created:
        content = instance
        for guideline in Guideline.objects.all():
            ReviewItem.objects.create(content=content, guideline=guideline)
