# Generated by Django 5.0.6 on 2024-06-18 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_profile_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='patronymic',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
