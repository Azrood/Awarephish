# Generated by Django 3.0.5 on 2020-05-03 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20200430_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reponses',
            name='correct_answer',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Réponse correct'),
        ),
    ]
