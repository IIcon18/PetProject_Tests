# Generated by Django 5.0.6 on 2024-06-18 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_delete_articles_alter_document_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={},
        ),
        migrations.RemoveField(
            model_name='document',
            name='anons',
        ),
        migrations.RemoveField(
            model_name='document',
            name='full_text',
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]