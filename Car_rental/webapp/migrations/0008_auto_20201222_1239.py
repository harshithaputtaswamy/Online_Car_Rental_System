# Generated by Django 3.1.2 on 2020-12-22 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20201222_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='amt',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.IntegerField(null=True),
        ),
    ]