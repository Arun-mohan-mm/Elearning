# Generated by Django 3.0.3 on 2020-04-03 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0054_auto_20200402_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Review', models.IntegerField()),
            ],
        ),
    ]