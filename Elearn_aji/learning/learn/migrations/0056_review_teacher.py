# Generated by Django 3.0.3 on 2020-04-03 04:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0055_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='Teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learn.Teacher_registration'),
            preserve_default=False,
        ),
    ]
