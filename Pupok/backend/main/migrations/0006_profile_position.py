# Generated by Django 5.0.6 on 2024-06-15 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='position',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
