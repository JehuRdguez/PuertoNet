# Generated by Django 5.0 on 2023-12-18 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_blogs_imagenesblogs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagenesblogs',
            name='IdBlog',
        ),
        migrations.DeleteModel(
            name='Blogs',
        ),
        migrations.DeleteModel(
            name='ImagenesBlogs',
        ),
    ]
