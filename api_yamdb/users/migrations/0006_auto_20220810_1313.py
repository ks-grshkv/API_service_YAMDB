# Generated by Django 2.2.16 on 2022-08-10 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20220810_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='ddddddvv', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(max_length=5),
        ),
    ]
