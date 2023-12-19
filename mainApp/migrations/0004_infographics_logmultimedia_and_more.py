# Generated by Django 5.0 on 2023-12-19 02:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Infographics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('format', models.IntegerField(choices=[(0, 'Imagen'), (1, 'Video')], default='0')),
                ('file', models.FileField(upload_to='files/')),
                ('category', models.IntegerField(choices=[(0, 'General'), (1, 'Principiantes'), (3, 'Kids')], default='0')),
                ('supplementary_Infographics', models.ManyToManyField(blank=True, null=True, to='mainApp.infographics')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LogMultimedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.CharField(max_length=20)),
                ('category', models.IntegerField(choices=[(0, 'General'), (1, 'Principiantes'), (3, 'Kids')], default='0')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('supplementary_Infographics', models.ManyToManyField(blank=True, null=True, to='mainApp.infographics')),
                ('supplementary_videos', models.ManyToManyField(blank=True, null=True, to='mainApp.logmultimedia')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='infographics',
            name='supplementary_videos',
            field=models.ManyToManyField(blank=True, null=True, to='mainApp.logmultimedia'),
        ),
    ]
