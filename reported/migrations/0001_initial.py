# Generated by Django 3.0.7 on 2021-05-31 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=140)),
                ('for_what', models.CharField(choices=[('U', 'User'), ('P', 'Post')], max_length=1)),
                ('max_reports', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': '     Report Types',
            },
        ),
        migrations.CreateModel(
            name='UserReportHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporting_time', models.DateTimeField(auto_now_add=True)),
                ('report_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reported.ReportTypes')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reported_by', to=settings.AUTH_USER_MODEL)),
                ('reported_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reported_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '   User Report History',
            },
        ),
        migrations.CreateModel(
            name='PostReportHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporting_time', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='video.MediaTable')),
                ('report_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reported.ReportTypes')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '  Post Report History',
            },
        ),
    ]