# Generated by Django 3.1.5 on 2021-02-11 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='duration',
            field=models.PositiveIntegerField(verbose_name='Время приготовления'),
        ),
    ]
