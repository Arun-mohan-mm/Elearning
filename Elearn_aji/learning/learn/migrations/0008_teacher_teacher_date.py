# Generated by Django 3.0.2 on 2020-01-15 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0007_remove_subject_details_teacher_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='teacher_date',
            field=models.CharField(max_length=200),
            preserve_default=False,
        ),
    ]