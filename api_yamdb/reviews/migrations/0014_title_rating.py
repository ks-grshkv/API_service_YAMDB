# Generated by Django 2.2.16 on 2022-08-14 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0013_remove_title_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.FloatField(default=5),
            preserve_default=False,
        ),
    ]