# Generated by Django 5.0.6 on 2024-07-10 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_testresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendedquestion',
            name='difficulty',
            field=models.CharField(choices=[('easy', 'Легкий'), ('medium', 'Средний'), ('hard', 'Сложный')], default='easy', max_length=6),
        ),
        migrations.AddField(
            model_name='question',
            name='difficulty',
            field=models.CharField(choices=[('easy', 'Легкий'), ('medium', 'Средний'), ('hard', 'Сложный')], default='easy', max_length=6),
        ),
    ]
