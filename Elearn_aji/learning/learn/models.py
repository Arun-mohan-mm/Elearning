from django.db import models

from django.contrib import admin

class Login(models.Model):
    Email = models.EmailField(max_length=200)
    Password = models.CharField(max_length=200)
    User_role = models.CharField(max_length=200)
class Admin_registration(models.Model):
    First_name = models.CharField(max_length=200)
    Last_name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    Password = models.CharField(max_length=200)
    Registration_date = models.DateField()
    Log_id = models.ForeignKey(Login, on_delete=models.CASCADE)
class Guest_contact(models.Model):
    Contact_name = models.CharField(max_length=200)
    Contact_email = models.EmailField(max_length=200)
    Contact_message = models.TextField()
class Student_registration(models.Model):
    First_name = models.CharField(max_length=200)
    Last_name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    Password = models.CharField(max_length=200)
    Registration_date = models.DateField()
    Num_of_courses_enrolled = models.IntegerField(default=0)
    Num_of_courses_completed = models.IntegerField(default=0)
    Log_id = models.ForeignKey(Login, on_delete=models.CASCADE)
class Teacher_registration(models.Model):
    First_name = models.CharField(max_length=200)
    Last_name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    Password = models.CharField(max_length=200)
    Registration_date = models.DateField()
    Qualification = models.CharField(max_length=200)
    Introduction_brief = models.TextField()
    Image = models.ImageField(upload_to='media')
    Num_of_enrolled_students = models.IntegerField()
    Average_review_rating = models.IntegerField()
    Num_of_reviews = models.IntegerField()
    Log_id = models.ForeignKey(Login, on_delete=models.CASCADE)
class Subject(models.Model):
    Subject_title = models.CharField(max_length=200)
    Course_title = models.CharField(max_length=200)
    Course_brief = models.TextField()
    Course_duration = models.IntegerField()
    Teacher_id = models.ForeignKey(Login, on_delete=models.CASCADE)
    Num_of_chapters = models.IntegerField()
    Course_fee = models.FloatField()
    Language = models.CharField(max_length=200)
class Course_chapter(models.Model):
    Subject_title = models.CharField(max_length=200)
    Course_name = models.CharField(max_length=200)
    Chapter_title = models.CharField(max_length=200)
    Num_of_videos = models.IntegerField()
    Num_of_paragraphs = models.IntegerField()
    Num_of_images = models.IntegerField()
    Num_of_assignments = models.IntegerField()
    Sub = models.ForeignKey(Subject, on_delete=models.CASCADE)
class Course_chapter_content(models.Model):
    Subject_title = models.CharField(max_length=200)
    Course_name = models.CharField(max_length=200)
    Course_chapter_name = models.CharField(max_length=200)
    Content_name = models.CharField(max_length=200)
    Content_type = models.CharField(max_length=200)
    Text_content = models.TextField(default='Nil')
    Is_mandatory = models.BooleanField()
    Time_required_in_sec = models.IntegerField()
    Is_open_for_free = models.BooleanField()
    Chapt = models.ForeignKey(Course_chapter, on_delete=models.CASCADE)
class Enrollment(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField()
    Subject_name = models.CharField(max_length=200)
    Course_name = models.CharField(max_length=200)
    Teacher_name = models.CharField(max_length=200)
    Teacher_email = models.EmailField()
    Attendance = models.IntegerField()
    Pending_days = models.IntegerField()
    Enrollment_date = models.DateField(auto_now_add=True)
    Teacher_response = models.CharField(max_length=200)
    Paid_amount = models.IntegerField()
    Is_paid_subscription = models.BooleanField()
class Learning_progress(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField()
    Subject_name = models.CharField(max_length=200)
    Course_name = models.CharField(max_length=200)
    Course_chapter_name = models.CharField(max_length=200)
    Course_chapter_content_name = models.CharField(max_length=200)
    Begin_timestamp = models.DateTimeField(auto_now_add=True)
    Completion_timestamp = models.DateTimeField(auto_now=True)
    Status = models.CharField(max_length=200)
class Feedback(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField()
    Subject_name = models.TextField()
    Course_name = models.TextField()
    Rating_score = models.IntegerField()
    Feedback_text = models.TextField(default='Nil')
    Submission_date = models.DateField()
class Messages(models.Model):
    Category = models.CharField(max_length=200)
    From_email = models.EmailField()
    To_email = models.EmailField()
    Message_content = models.TextField(default='Nil')
class Certificates(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField()
    Certificate = models.CharField(max_length=200)
class Requests(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField()
    User_category = models.CharField(max_length=200)
    Old_password = models.CharField(max_length=200)
    New_password = models.CharField(max_length=200)
class Exam(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField()
    Teacher_name = models.CharField(max_length=200)
    Subject_name = models.CharField(max_length=200)
    Course_name = models.CharField(max_length=200)
    Lock = models.CharField(max_length=200)
    Question = models.TextField()
    Option1 = models.TextField()
    Option2 = models.TextField()
    Option3 = models.TextField()
    Correct_answer = models.TextField()
    Time_start = models.DateTimeField()
    Time_stop = models.DateTimeField()
class Exam_results(models.Model):
    Student_name = models.CharField(max_length=200)
    Student_email = models.EmailField(max_length=200)
    Teacher_name = models.CharField(max_length=200)
    Subject_name = models.CharField(max_length=200)
    Total_marks = models.IntegerField()
    Acquired_marks = models.IntegerField()
    Grade = models.CharField(max_length=200)
    Time_stop = models.DateTimeField(auto_now=True)
class About(models.Model):
    About = models.TextField()
class Blogs(models.Model):
    Name = models.CharField(max_length=200)
    Blog_content = models.TextField()
    Image = models.ImageField()
    Date_blog = models.DateField()
    Approval_status = models.CharField(max_length=200)

class Review(models.Model):
    Review = models.IntegerField()
    Teacher = models.ForeignKey(Teacher_registration, on_delete=models.CASCADE)