# Generated by Django 4.1.4 on 2022-12-15 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='name',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
    ]
