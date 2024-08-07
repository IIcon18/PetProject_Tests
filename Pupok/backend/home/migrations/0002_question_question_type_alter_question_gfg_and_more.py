# Generated by Django 5.0.6 on 2024-06-14 10:22

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('MCQ', 'Multiple Choice Question'), ('SA', 'Short Answer')], default='MCQ', max_length=3),
        ),
        migrations.AlterField(
            model_name='question',
            name='gfg',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='home.types'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='ExtendedAnswer',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('text', models.TextField(verbose_name='Текст ответа')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Правильный ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extended_answers', to='home.question')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
