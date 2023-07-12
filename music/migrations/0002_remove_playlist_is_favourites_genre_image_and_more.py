# Generated by Django 4.2.3 on 2023-07-10 13:15

import Stream.yandex_s3_storage
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='is_favourites',
        ),
        migrations.AddField(
            model_name='genre',
            name='image',
            field=models.FileField(blank=True, null=True, storage=Stream.yandex_s3_storage.ClientDocsStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='duration_time',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.CreateModel(
            name='FavoriteTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_date', models.DateTimeField(auto_now_add=True)),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.track', verbose_name='Трек')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
