# Generated by Django 3.0.7 on 2021-05-31 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import login_signup.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notification_and_mails', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlackListedAccessTokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=250)),
                ('blacklisted_at', models.FloatField(default=login_signup.models.get_timestamp)),
            ],
        ),
        migrations.CreateModel(
            name='UserXBlockedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blocked_at', models.DateTimeField(auto_now_add=True)),
                ('blocked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_by', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Block Panel',
            },
        ),
        migrations.CreateModel(
            name='UserCrossFollower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_at', models.DateTimeField(auto_now_add=True)),
                ('followed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to=settings.AUTH_USER_MODEL)),
                ('notification_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='notification_and_mails.NotificationHistory')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '  Follow Panel',
            },
        ),
        migrations.CreateModel(
            name='Social_Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook', models.BooleanField(default=False, null=True)),
                ('facebook_id', models.CharField(max_length=255, null=True)),
                ('google', models.BooleanField(default=False, null=True)),
                ('google_id', models.CharField(max_length=255, null=True)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(choices=[('1', 'ENGLISH')], max_length=1)),
                ('device_id', models.CharField(max_length=50)),
                ('device_info', models.CharField(max_length=250)),
                ('app_info', models.CharField(max_length=20)),
                ('device_token', models.CharField(max_length=250)),
                ('device_type', models.CharField(choices=[('A', 'Android'), ('I', 'IOS'), ('W', 'WebApp')], max_length=1)),
                ('authorization_token', models.CharField(max_length=250)),
                ('user_token', models.CharField(max_length=50)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('mobile_no', models.CharField(max_length=25, unique=True)),
                ('display_picture', models.ImageField(default='defaults/display_picture.jpg', null=True, upload_to=login_signup.models.AppUser.get_upload_path_display_picture)),
                ('cover_picture', models.ImageField(default='defaults/cover_picture.jpg', null=True, upload_to=login_signup.models.AppUser.get_upload_path_cover_photo)),
                ('location', models.CharField(default=None, max_length=70, null=True)),
                ('city', models.CharField(default=None, max_length=25, null=True)),
                ('state', models.CharField(default=None, max_length=25, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('N', None)], default=None, max_length=1, null=True)),
                ('age', models.IntegerField(default=None, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('about', models.CharField(default=None, max_length=140, null=True)),
                ('user_link', models.CharField(default=None, max_length=100, null=True)),
                ('twitter_handle', models.CharField(default=None, max_length=50, null=True)),
                ('address', models.CharField(default=None, max_length=250, null=True)),
                ('otp_time', models.FloatField(default=login_signup.models.get_timestamp)),
                ('is_profile_completed', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_phone_verified', models.BooleanField(default=True)),
                ('hash_key', models.CharField(default=None, max_length=200, null=True)),
                ('website', models.CharField(default=None, max_length=50, null=True)),
                ('ref_code', models.CharField(default=None, max_length=100, null=True)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '   Profile Details',
            },
        ),
    ]
