# Generated by Django 4.2.4 on 2023-10-24 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
