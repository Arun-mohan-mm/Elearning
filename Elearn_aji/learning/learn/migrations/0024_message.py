# Generated by Django 3.0.2 on 2020-02-04 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0023_auto_20200204_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('rec_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('msg', models.TextField(max_length=200)),
            ],
        ),
    ]
