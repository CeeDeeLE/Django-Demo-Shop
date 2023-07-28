# Generated by Django 4.2.2 on 2023-07-18 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artikel',
            name='preis',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='kunde',
            name='email',
            field=models.EmailField(max_length=200, null=True),
        ),
    ]
