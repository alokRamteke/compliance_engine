# Generated by Django 5.0.4 on 2024-04-25 04:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewitem',
            name='review',
        ),
        migrations.AlterModelOptions(
            name='guideline',
            options={'verbose_name': 'Compliance Guideline', 'verbose_name_plural': 'Compliance Guidelines'},
        ),
        migrations.AddField(
            model_name='reviewitem',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_items', to='core.content'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reviewitem',
            name='reviewer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='content',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reviewitem',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PASS', 'Passed'), ('FAIL', 'Failed')], default='PENDING', max_length=10),
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
