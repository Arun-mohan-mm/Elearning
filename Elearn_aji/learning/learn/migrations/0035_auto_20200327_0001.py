# Generated by Django 3.0.3 on 2020-03-26 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0034_auto_20200325_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='Enrollment_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
