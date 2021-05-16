# Generated by Django 3.2.1 on 2021-05-16 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userfollowing',
            name='unique_user_following',
        ),
        migrations.RenameField(
            model_name='userfollowing',
            old_name='follower_user',
            new_name='follower_user_id',
        ),
        migrations.RenameField(
            model_name='userfollowing',
            old_name='following_user',
            new_name='following_user_id',
        ),
        migrations.AddConstraint(
            model_name='userfollowing',
            constraint=models.UniqueConstraint(fields=('follower_user_id', 'following_user_id'), name='unique_user_following'),
        ),
    ]
