# Generated by Django 4.2 on 2023-05-07 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profilepage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepage',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='media'),
        ),
    ]
