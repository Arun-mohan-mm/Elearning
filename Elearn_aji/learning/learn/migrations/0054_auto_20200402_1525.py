# Generated by Django 3.0.3 on 2020-04-02 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0053_course_chapter_content_text_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learning_progress',
            name='Begin_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='learning_progress',
            name='Completion_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
