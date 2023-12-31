# Generated by Django 4.1.2 on 2023-08-17 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('song_id', models.CharField(max_length=255)),
                ('album', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('album_cover', models.URLField()),
                ('year_release_date', models.CharField(max_length=4)),
                ('genres', models.JSONField()),
                ('duration', models.CharField(max_length=255)),
                ('origin', models.CharField(max_length=255)),
            ],
        ),
    ]
