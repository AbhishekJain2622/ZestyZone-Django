# Generated by Django 5.1.4 on 2024-12-26 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Offer_name', models.CharField(max_length=100)),
                ('Offer', models.CharField(max_length=50)),
                ('img', models.ImageField(upload_to='images')),
            ],
        ),
    ]
