# Generated by Django 3.0.3 on 2020-04-01 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0049_exam_results_lock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam_results',
            name='Lock',
        ),
    ]