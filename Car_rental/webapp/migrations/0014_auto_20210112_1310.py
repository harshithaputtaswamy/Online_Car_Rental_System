# Generated by Django 3.1.2 on 2021-01-12 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_auto_20210112_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phno',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
