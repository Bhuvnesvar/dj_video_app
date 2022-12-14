# Generated by Django 3.0.7 on 2021-05-31 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EffectsAndFilters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='defaults/effects_and_filters/')),
                ('thumbnail', models.FileField(upload_to='defaults/effects_and_filters/')),
                ('type', models.CharField(choices=[('E', 'Effects'), ('F', 'Filters')], max_length=1)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Effects And Filters',
            },
        ),
    ]
