# Generated by Django 5.0 on 2023-12-19 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0011_alter_blogs_autor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='autor',
            field=models.TextField(blank=True, null=True),
        ),
    ]
