# Generated by Django 5.0.6 on 2024-06-22 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_extendedquestion_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.CharField(max_length=200),
        ),
    ]
