# Generated by Django 3.0.3 on 2020-03-03 02:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('learn', '0027_auto_20200303_0806'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('About', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Blog_content', models.TextField()),
                ('Image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Certificates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Student_name', models.CharField(max_length=200)),
                ('Student_email', models.EmailField(max_length=254)),
                ('Certificate', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Course_chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Subject_title', models.CharField(max_length=200)),
                ('Course_name', models.CharField(max_length=200)),
                ('Chapter_title', models.CharField(max_length=200)),
                ('Num_of_videos', models.IntegerField()),
                ('Num_of_assignments', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Course_chapter_content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Subject_title', models.CharField(max_length=200)),
                ('Course_name', models.CharField(max_length=200)),
                ('Course_chapter_name', models.CharField(max_length=200)),
                ('Content_type', models.CharField(max_length=200)),
                ('Is_mandatory', models.BooleanField()),
                ('Time_required_in_sec', models.IntegerField()),
                ('Is_open_for_free', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Student_name', models.CharField(max_length=200)),
                ('Student_email', models.EmailField(max_length=254)),
                ('Subject_name', models.CharField(max_length=200)),
                ('Course_name', models.CharField(max_length=200)),
                ('Teacher_name', models.CharField(max_length=200)),
                ('Teacher_email', models.EmailField(max_length=254)),
                ('Attendance', models.IntegerField()),
                ('Pending_days', models.IntegerField()),
                ('Enrollment_date', models.DateField()),
                ('Teacher_response', models.BooleanField()),
                ('Is_paid_subscription', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Student_name', models.CharField(max_length=200)),
                ('Teacher_name', models.CharField(max_length=200)),
                ('Subject_name', models.CharField(max_length=200)),
                ('Questions', models.TextField()),
                ('Answers', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Exam_results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Student_name', models.CharField(max_length=200)),
                ('Teacher_name', models.CharField(max_length=200)),
                ('Subject_name', models.CharField(max_length=200)),
                ('Total_marks', models.IntegerField()),
                ('Acquired_marks', models.IntegerField()),
                ('Grade', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Student_name', models.CharField(max_length=200)),
                ('Student_email', models.EmailField(max_length=254)),
                ('Subject_name', models.CharField(max_length=200)),
                ('Course_name', models.CharField(max_length=200)),
                ('Rating_score', models.IntegerField()),
                ('Feedback_text', models.TextField(default='Nil')),
                ('Submission_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Learning_progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Student_name', models.CharField(max_length=200)),
                ('Student_email', models.EmailField(max_length=254)),
                ('Subject_name', models.CharField(max_length=200)),
                ('Course_name', models.CharField(max_length=200)),
                ('Course_chapter_content_name', models.CharField(max_length=200)),
                ('Begin_timestamp', models.DateTimeField()),
                ('Completion_timestamp', models.DateTimeField()),
                ('Status', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=200)),
                ('Password', models.CharField(max_length=200)),
                ('User_role', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(max_length=200)),
                ('From_email', models.EmailField(max_length=254)),
                ('To_email', models.EmailField(max_length=254)),
                ('Message_content', models.TextField(default='Nil')),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Email', models.EmailField(max_length=254)),
                ('User_category', models.CharField(max_length=200)),
                ('Old_password', models.CharField(max_length=200)),
                ('New_password', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher_registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_name', models.CharField(max_length=200)),
                ('Last_name', models.CharField(max_length=200)),
                ('Email', models.EmailField(max_length=200)),
                ('Password', models.CharField(max_length=200)),
                ('Registration_date', models.DateField()),
                ('Qualification', models.CharField(max_length=200)),
                ('Introduction_brief', models.TextField()),
                ('Image', models.ImageField(upload_to='')),
                ('Num_of_enrolled_students', models.IntegerField()),
                ('Average_review_rating', models.IntegerField()),
                ('Num_of_reviews', models.IntegerField()),
                ('Log_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learn.Login')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Subject_title', models.CharField(max_length=200)),
                ('Course_title', models.CharField(max_length=200)),
                ('Course_brief', models.TextField()),
                ('Course_duration', models.IntegerField()),
                ('Num_of_chapters', models.IntegerField()),
                ('Course_fee', models.FloatField()),
                ('Language', models.CharField(max_length=200)),
                ('Teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learn.Teacher_registration')),
            ],
        ),
        migrations.CreateModel(
            name='Student_registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_name', models.CharField(max_length=200)),
                ('Last_name', models.CharField(max_length=200)),
                ('Email', models.EmailField(max_length=200)),
                ('Password', models.CharField(max_length=200)),
                ('Registration_date', models.DateField()),
                ('Num_of_courses_enrolled', models.IntegerField(default=0)),
                ('Num_of_courses_completed', models.IntegerField(default=0)),
                ('Log_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learn.Login')),
            ],
        ),
        migrations.CreateModel(
            name='Admin_registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_name', models.CharField(max_length=200)),
                ('Last_name', models.CharField(max_length=200)),
                ('Email', models.EmailField(max_length=200)),
                ('Password', models.CharField(max_length=200)),
                ('Registration_date', models.DateField()),
                ('Log_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learn.Login')),
            ],
        ),
    ]
