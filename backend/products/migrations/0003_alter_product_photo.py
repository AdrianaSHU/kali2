# Generated by Django 5.1.4 on 2024-12-18 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, default='path/to/default_image.jpg', null=True, upload_to='product_photos/'),
        ),
    ]
