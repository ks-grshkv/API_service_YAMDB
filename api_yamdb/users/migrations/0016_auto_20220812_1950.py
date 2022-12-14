# Generated by Django 2.2.16 on 2022-08-12 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20220811_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='00000', max_length=5),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'Администратор'), ('admin', 'Пользователь'), ('moderator', 'Модератор')], default='user', max_length=10),
        ),
    ]
