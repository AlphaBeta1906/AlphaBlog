# Generated by Django 4.0.6 on 2022-07-09 08:35

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_alter_post_date_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=markdownx.models.MarkdownxField(max_length=10000000),
        ),
    ]
