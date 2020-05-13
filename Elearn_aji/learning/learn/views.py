from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
from django.contrib import messages
import requests
from learn.forms import LoginForm
import pandas as pd
from bs4 import BeautifulSoup
import time
import datetime
import re
from datetime import date
from django.core import serializers
import json
from django.core.files.storage import FileSystemStorage
import pytz
from django.utils import timezone

def home(request):
    sdd = Subject.objects.all()
    sd = []
    for i in sdd:
        if i.Subject_title not in sd:
            sd.append(i.Subject_title)
    return render(request,'home.html',{'sd':sd})
def add_blog(request):
    if request.method == 'POST':
        nam = request.POST.get('nam')
        c_b = request.POST.get('c_b')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        date1 = request.POST.get('date1')
        b = Blogs()
        b.Name = nam
        b.Blog_content = c_b
        b.Image = photo
        b.Date_blog = date1
        b.Approval_status = 'Rejected'
        b.save()
        messages.success(request, 'Blog added successfully. Please wait for approval')
        return render(request, 'home.html')
    return render(request,'add_blog.html')

def blogs_admin(request):
    dm = Blogs.objects.all()
    return render(request,'blogs_admin.html',{'dm':dm})

def blog_approves(request,id):
    sas = Blogs.objects.get(id=id)
    sas.Approval_status = 'Approved'
    sas.save()
    dm = Blogs.objects.all()
    return render(request, 'blogs_admin.html', {'dm': dm})

def blog_rejects(request, id):
    sas = Blogs.objects.get(id=id)
    sas.Approval_status = 'Rejected'
    sas.save()
    dm = Blogs.objects.all()
    return render(request, 'blogs_admin.html', {'dm': dm})

def blog_delete(request, id):
    Blogs.objects.get(id=id).delete()
    dm = Blogs.objects.all()
    return render(request, 'blogs_admin.html', {'dm': dm})

def view_blog(request):
    dc = Blogs.objects.filter(Approval_status = 'Approved')
    return render(request,'display_blog.html',{'dc':dc})

def reg_msg(request):
    sdd = Subject.objects.all()
    sd = []
    for i in sdd:
        if i.Subject_title not in sd:
            sd.append(i.Subject_title)
    messages.success(request, 'Please register to access course contents')
    return render(request, 'home.html',{'sd':sd})

def about(request):
    df = About.objects.all()
    bn = Teacher_registration.objects.all()
    return render(request,'about.html',{'df':df,'bn':bn})

def abb(request):
    amm = About.objects.all()
    if request.method == 'POST':
        ss = Student_registration.objects.all()
        tt = Teacher_registration.objects.all()
        abbt = request.POST.get('abbt')
        idd = request.POST.get('idd')
        try:
            adc = About.objects.get(id = idd)
            adc.About = abbt
            adc.save()
            messages.success(request, 'Content added successfully')
            return render(request, "admin_home.html", {'ss': ss, 'tt': tt})
        except:
            adc = About()
            adc.About = abbt
            adc.save()
            messages.success(request, 'Content added successfully')
            return render(request, "admin_home.html", {'ss': ss, 'tt': tt})
    return render(request,'about_content.html',{'amm':amm})

def home1(request):
    return render(request,'index.html')
def k(request):
    return render(request,'k.html')
def admin_home(request):
    ss = Student_registration.objects.all()
    tt = Teacher_registration.objects.all()
    return render(request, "admin_home.html", {'ss': ss, 'tt': tt})

def register_st(request):
    if request.method == 'POST':
        x = datetime.datetime.now()
        y = x.strftime("%Y-%m-%d")
        typ = request.POST.get('student')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        log = Login()
        log.Email = email
        log.Password = psw
        log.User_role = typ
        log.save()
        reg = Student_registration()
        reg.First_name = first_name
        reg.Last_name = last_name
        reg.Email = email
        reg.Password = psw
        reg.user_category = typ
        reg.Registration_date = y
        reg.Log_id = log
        reg.save()
        messages.success(request, 'You have successfully registered')
        return render(request, 'home.html')
    else:
        return render(request, 'register.html')

def register_tr(request):
    if request.method == 'POST':
        x = datetime.datetime.now()
        y = x.strftime("%Y-%m-%d")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')
        photo = request.FILES['photo']
        """fs = FileSystemStorage()
        fs.save(photo.name, photo)"""
        enrol = request.POST.get('enrol')
        avg_rev = request.POST.get('avg_rev')
        tot_rev = request.POST.get('tot_rev')
        teach = request.POST.get('teacher')
        log = Login()
        log1 = Login.objects.all()
        for i in log1:
            if i.Email == email:
                messages.success(request, 'User already exists')
                return render(request, 'home.html')
        log.Email = email
        log.Password = psw
        log.User_role = teach
        log.save()
        t = Teacher_registration()
        t.First_name = first_name
        t.Last_name = last_name
        t.Email = email
        t.Password = psw
        t.Registration_date = y
        t.Qualification = qual
        t.Introduction_brief = intro
        t.Image = photo
        t.Num_of_enrolled_students = enrol
        t.Average_review_rating = avg_rev
        t.Num_of_reviews = tot_rev
        t.Log_id = log
        t.save()
        messages.success(request, 'You have successfully registered')
        return render(request, 'home.html')
    else:
        return render(request, 'register_teacher.html')
def admin_rg(request):
    if request.method == 'POST':
        lk = Login.objects.all()
        for t in lk:
            if t.User_role == 'admin':
                messages.success(request, 'You are not allowed to be registered as admin')
                return render(request, 'home.html')
        x = datetime.datetime.now()
        z = x.strftime("%Y-%m-%d")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        admin = request.POST.get('adminn1')
        log = Login()
        log1 = Login.objects.all()
        for i in log1:
            if i.Email == email:
                messages.success(request, 'User already exists')
                return render(request, 'home.html')
        log.Email = email
        log.Password = psw
        log.User_role = admin
        log.save()
        t = Admin_registration()
        t.First_name = first_name
        t.Last_name = last_name
        t.Email = email
        t.Password = psw
        t.Registration_date = z
        t.Log_id = log
        t.save()
        messages.success(request, 'You have successfully registered')
        return render(request, 'home.html')
    else:
        return render(request, 'register_admin.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get("email")
        password = request.POST.get("pword")
        if (Login.objects.filter(Email=username, Password=password).exists()):
            logs = Login.objects.filter(Email=username, Password=password)

            for value in logs:
                user_id = value.id
                usertype  = value.User_role
                if usertype == 'admin':
                    czc = Course_chapter_content.objects.all()
                    bzb = Course_chapter.objects.all()
                    for ii in bzb:
                        gg = 0
                        ggw = 0
                        ggy = 0
                        for kk in czc:
                            if kk.Content_type == 'Image' and kk.Course_chapter_name == ii.Chapter_title:
                                gg += 1
                                ii.Num_of_images = int(gg)
                            if kk.Content_type == 'Video' and kk.Course_chapter_name == ii.Chapter_title:
                                ggw += 1
                                ii.Num_of_videos = int(ggw)
                            if kk.Content_type == 'Text' and kk.Course_chapter_name == ii.Chapter_title:
                                ggy += 1
                                ii.Num_of_paragraphs = int(ggy)
                        ii.save()
                    ss = Student_registration.objects.all()
                    tt = Teacher_registration.objects.all()
                    request.session['logg'] = user_id
                    return render(request, "admin_home.html",{'ss':ss,'tt':tt})

                elif usertype == 'teacher':
                    czc = Course_chapter_content.objects.all()
                    bzb = Course_chapter.objects.all()
                    for ii in bzb:
                        gg = 0
                        ggw = 0
                        ggy = 0
                        for kk in czc:
                            if kk.Content_type == 'Image' and kk.Course_chapter_name == ii.Chapter_title:
                                gg += 1
                                ii.Num_of_images = int(gg)
                            if kk.Content_type == 'Video' and kk.Course_chapter_name == ii.Chapter_title:
                                ggw += 1
                                ii.Num_of_videos = int(ggw)
                            if kk.Content_type == 'Text' and kk.Course_chapter_name == ii.Chapter_title:
                                ggy += 1
                                ii.Num_of_paragraphs = int(ggy)
                        ii.save()
                    request.session['logg'] = user_id
                    bb = Login.objects.get(id = request.session['logg'])
                    dm = Enrollment.objects.filter(Teacher_email = bb.Email)
                    cou = []
                    for i in dm:
                        if i.Student_email not in cou:
                            cou.append(i.Student_email)
                    fd = 0
                    for y in cou:
                        fd+=1
                    vn = Teacher_registration.objects.get(Email = bb.Email)
                    vn.Num_of_enrolled_students = fd
                    vn.save()
                    return render(request, 'teacher_home.html')

                elif usertype == 'student':
                    czc = Course_chapter_content.objects.all()
                    bzb = Course_chapter.objects.all()
                    for ii in bzb:
                        gg = 0
                        ggw = 0
                        ggy = 0
                        for kk in czc:
                            if kk.Content_type == 'Image' and kk.Course_chapter_name == ii.Chapter_title:
                                gg += 1
                                ii.Num_of_images = int(gg)
                            if kk.Content_type == 'Video' and kk.Course_chapter_name == ii.Chapter_title:
                                ggw += 1
                                ii.Num_of_videos = int(ggw)
                            if kk.Content_type == 'Text' and kk.Course_chapter_name == ii.Chapter_title:
                                ggy += 1
                                ii.Num_of_paragraphs = int(ggy)
                        ii.save()
                    request.session['logg'] = user_id
                    g = Enrollment.objects.all()
                    b = Login.objects.all()
                    for i in g:
                        for k in b:
                            if i.Student_email == k.Email:
                                n = Student_registration.objects.get(Email = k.Email)
                                n.Num_of_courses_enrolled = 0
                                n.save()
                    for i in g:
                        for k in b:
                            if i.Student_email == k.Email:
                                qq = Course_chapter_content.objects.filter(Subject_title = i.Subject_name, Course_name = i.Course_name)
                                qq1 = Learning_progress.objects.filter(Student_email = k.Email)
                                for aq in qq1:
                                    if k.Email == aq.Student_email:
                                        cot = []
                                        for u in qq:
                                            for zz in qq1:
                                                if zz.Status == 'P':
                                                    if zz.Course_name not in cot:
                                                        cot.append(zz.Course_name)
                                        count = 0
                                        for r in cot:
                                            count += 1
                                        mbm = Enrollment.objects.filter(Student_email = k.Email)
                                        cott = []
                                        for w in mbm:
                                            if w.Course_name not in cott:
                                                cott.append(w.Course_name)
                                        cnt = 0
                                        for q in cott:
                                            cnt+=1
                                        bbb = 0
                                        for x in cott:
                                            if x not in cot:
                                                bbb += 1
                                        nn = Student_registration.objects.get(Email=k.Email)
                                        nn.Num_of_courses_completed = bbb
                                n = Student_registration.objects.get(Email=k.Email)
                                n.Num_of_courses_enrolled += 1
                                n.save()
                                delta = datetime.datetime.now().date() - i.Enrollment_date
                                d = int(delta.days)
                                try:
                                    df = Subject.objects.get(Subject_title = i.Subject_name, Course_title = i.Course_name)
                                    st = int(df.Course_duration)
                                    st1 = st - d
                                    i.Pending_days = st1
                                    i.save()
                                except:
                                    i.save()

                    return render(request, 'student_home.html')
                else:
                    messages.success(request, 'Your access to the website is blocked. Please contact admin')
                    return render(request, 'login.html')
        else:
            messages.success(request, 'Email or password entered is incorrect')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def student_home(request):
    return render(request, "student_home.html")

def teacher_home(request):
    return render(request, 'teacher_home.html')



def news(request):
    page = requests.get('https://www.indiatoday.in/education-today')
    soup = BeautifulSoup(page.content,'html.parser')
    week = soup.find(class_ = 'special-top-news')
    wm = week.find(class_ = 'itg-listing')
    w = wm.find_all('a')
    ww = []
    for x in w:
        ww.append(x.get_text())
    x = datetime.datetime.now()
    return render(request,'news.html',{'ww':ww,'x':x})

def stu_buk_acc(request):
    seww = Login.objects.get(id = request.session['logg'])
    stzz = Enrollment.objects.filter(Teacher_email = seww.Email)
    return render(request,'stu_buk_acc.html',{'stzz':stzz})

def stu_delete(request, id):
    dt = Enrollment.objects.get(id=id)
    Learning_progress.objects.filter(Student_email = dt.Student_email, Subject_name = dt.Subject_name, Course_name = dt.Course_name, Status = 'C').delete()
    Enrollment.objects.get(id = id).delete()
    seww = Login.objects.get(id = request.session['logg'])
    stzz = Enrollment.objects.filter(Teacher_email = seww.Email)
    messages.success(request, 'Enrolled student deleted successfully')
    return render(request, 'stu_buk_acc.html', {'stzz': stzz})

def stu_accept(request, id):
    seww = Login.objects.get(id=request.session['logg'])
    stzz = Enrollment.objects.filter(Teacher_email=seww.Email)
    sas = Enrollment.objects.get(id = id)
    sas.Teacher_response = 'Accepted'
    sas.save()
    return render(request,'stu_buk_acc.html',{'stzz':stzz})

def stu_reject(request, id):
    seww = Login.objects.get(id=request.session['logg'])
    stzz = Enrollment.objects.filter(Teacher_email=seww.Email)
    sas = Enrollment.objects.get(id=id)
    sas.Teacher_response = 'Rejected'
    sas.save()
    return render(request, 'stu_buk_acc.html', {'stzz': stzz})

def sched_test(request):
    sew = Login.objects.get(id = request.session['logg'])
    stz = Enrollment.objects.filter(Teacher_email = sew.Email, Teacher_response = 'Accepted')
    return render(request,'sched_test.html',{'stz':stz})

def sched_test1(request):
    numbb = request.POST.get('numbb')
    nmbb = int(numbb)
    request.session['exam_start'] = dtt = request.POST.get('dtt')
    request.session['exam_stop'] = stt = request.POST.get('stt')
    request.session['cc'] = nmbb
    k = request.POST.getlist('scd')
    request.session['stu_for_test'] = k
    return render(request,'sched_test2.html')

def sched_test3(request):
    m = request.session['stu_for_test']
    ques = request.POST.get('ques')
    op1 = request.POST.get('op1')
    op2 = request.POST.get('op2')
    op3 = request.POST.get('op3')
    ans = request.POST.get('ans')
    c = request.session['cc']
    if c>0:
        for i in m:
            stz = Enrollment.objects.get(id = i)
            fd = Exam()
            fd.Student_name = stz.Student_name
            fd.Student_email = stz.Student_email
            fd.Teacher_name = stz.Teacher_name
            fd.Subject_name = stz.Subject_name
            fd.Course_name = stz.Course_name
            fd.Option1 = op1
            fd.Option2 = op2
            fd.Option3 = op3
            fd.Correct_answer = ans
            fd.Question = ques
            fd.Time_start = request.session['exam_start']
            fd.Time_stop = request.session['exam_stop']
            fd.save()
        c -= 1
        request.session['cc'] = c
        if c == 0:
            messages.success(request, 'Exam scheduled successfully')
            return render(request, 'teacher_home.html')
        return render(request,'sched_test2.html')
    else:
        messages.success(request, 'Exam scheduled successfully')
        return render(request, 'teacher_home.html')

def ex_not(request):
    local_tz = pytz.timezone("Asia/Calcutta")
    hh = Login.objects.get(id = request.session['logg'])
    fg = Exam.objects.filter(Student_email = hh.Email)
    kk = []
    for i in fg:
        bb = i.Time_start
        cpp = bb.replace(tzinfo=pytz.utc).astimezone(local_tz)
        bbn = cpp.strftime("%Y-%B-%d %H:%M:%S %p")
        if bbn not in kk:
            kk.append('Subject name')
            kk.append(i.Subject_name)
            kk.append('Course name')
            kk.append(i.Course_name)
            kk.append('Start time')
            ft = i.Time_start
            ftt = ft.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty = ftt.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty)
            kk.append('Stop time')
            fte = i.Time_stop
            ftee = fte.replace(tzinfo=pytz.utc).astimezone(local_tz)
            fty1 = ftee.strftime("%Y-%B-%d %H:%M:%S %p")
            kk.append(fty1)
    return render(request,'ex_not.html',{'kk':kk})
def update_pr_tr(request):
    bb = Teacher_registration.objects.get(Log_id=request.session['logg'])
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')
        try:
            imgg1 = request.FILES['imgg1']
            fs = FileSystemStorage()
            fs.save(imgg1.name,imgg1)
            enrol = request.POST.get('enrol')
            log = Login.objects.get(id=request.session['logg'])
            log.Email = email
            log.save()
            bb.First_name = f_name
            bb.Last_name = l_name
            bb.Email = email
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg1
            bb.Num_of_enrolled_students = enrol
            bb.save()
            messages.success(request, 'Updated successfully')
            return render(request, 'teacher_home.html')
        except:
            imgg2 = request.POST.get('imgg2')
            enrol = request.POST.get('enrol')
            log = Login.objects.get(id=request.session['logg'])
            log.Email = email
            log.save()
            bb.First_name = f_name
            bb.Last_name = l_name
            bb.Email = email
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg2
            bb.Num_of_enrolled_students = enrol
            bb.save()
            messages.success(request, 'Updated successfully')
            return render(request, 'teacher_home.html')
    return render(request, 'update_pr_tr.html', {'bb': bb})

def logout(request):
    if 'logg' in request.session:
        del request.session['logg']
        return render(request,'home.html')
    return render(request, 'home.html')
def update_pr_st(request):
    b = Student_registration.objects.get(Log_id = request.session['logg'])
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        log = Login.objects.get(id = request.session['logg'])
        log.Email = email
        log.save()
        b.First_name = f_name
        b.Last_name = l_name
        b.Email = email
        b.save()
        messages.success(request, 'Profile updated')
        return render(request,'student_home.html')
    return render(request, 'update_pr_st.html', {'b': b})

def course_name(request, id):
    dd = Subject_details.objects.filter(sub_name = id)
    return render(request, 'teacher_home.html', {'dd': dd})

def subject_tr(request):
   dd = Subject.objects.filter(Teacher_id = request.session['logg'])
   return render(request,'sub_tr.html',{'dd':dd})

def subject_ad(request):
   mm = Login.objects.all()
   dd = Subject.objects.all()
   gt = Teacher_registration.objects.all()
   return render(request,'sub_ad.html',{'dd':dd,'gt':gt,'mm':mm})

def edit_subject1(request, id):
    gh = Subject.objects.get(id = id)
    dd = Subject.objects.all()
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_b = request.POST.get('c_b')
        c_d = request.POST.get('c_d')
        n_c = request.POST.get('n_c')
        c_f = request.POST.get('c_f')
        lan = request.POST.get('lan')
        gh.Subject_title = sub
        gh.Course_title = cou
        gh.Course_brief = c_b
        gh.Course_duration = c_d
        gh.Num_of_chapters = n_c
        gh.Course_fee  = c_f
        gh.Language  = lan
        gh.save()
        messages.success(request, 'Subject edited successfully')
        return render(request, 'sub_ad.html',{'dd':dd})
    return render(request,'edit_subject1.html',{'gh':gh})

def edit_subject(request, id):
    gh = Subject.objects.get(id = id)
    dd = Subject.objects.filter(Teacher_id = request.session['logg'])
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_b = request.POST.get('c_b')
        c_d = request.POST.get('c_d')
        n_c = request.POST.get('n_c')
        c_f = request.POST.get('c_f')
        lan = request.POST.get('lan')
        gh.Subject_title = sub
        gh.Course_title = cou
        gh.Course_brief = c_b
        gh.Course_duration = c_d
        gh.Num_of_chapters = n_c
        gh.Course_fee  = c_f
        gh.Language  = lan
        gh.save()
        messages.success(request, 'Subject edited successfully')
        return render(request, 'sub_tr.html',{'dd':dd})
    return render(request,'edit_subject.html',{'gh':gh})

def delete_subject1(request, id):
    Subject.objects.get(id=id).delete()
    dd = Subject.objects.all()
    messages.success(request, 'Deleted subject successfully')
    return render(request, 'sub_ad.html', {'dd': dd})

def delete_subject(request, id):
    Subject.objects.get(id = id).delete()
    dd = Subject.objects.filter(Teacher_id = request.session['logg'])
    messages.success(request, 'Deleted subject successfully')
    return render(request, 'sub_tr.html',{'dd':dd})

def add_subject(request):
    dd = Subject.objects.filter(Teacher_id = request.session['logg'])
    if request.method == 'POST':
        sub_tit = request.POST.get('sub_tit')
        cou_tit = request.POST.get('cou_tit')
        c_b1 = request.POST.get('c_b1')
        c_d1 = request.POST.get('c_d1')
        n_c1 = request.POST.get('n_c1')
        c_f1 = request.POST.get('c_f1')
        lang = request.POST.get('lang')
        pk = Login.objects.get(id = request.session['logg'])
        cdt = Subject()
        cdt.Subject_title = sub_tit
        cdt.Course_title = cou_tit
        cdt.Course_brief = c_b1
        cdt.Course_duration = c_d1
        cdt.Num_of_chapters = n_c1
        cdt.Course_fee = c_f1
        cdt.Language = lang
        cdt.Teacher_id = pk
        cdt.save()
        messages.success(request, 'Added subject successfully')
        return render(request, 'sub_tr.html', {'dd': dd})
    return render(request,'add_subject.html')

def chapter_tr(request):
    dm = Subject.objects.filter(Teacher_id = request.session['logg'])
    dd = Course_chapter.objects.all()
    czc = Course_chapter_content.objects.all()
    bzb = Course_chapter.objects.all()
    for ii in bzb:
        gg = 0
        ggw = 0
        ggy = 0
        for kk in czc:
            if kk.Content_type == 'Image' and kk.Course_chapter_name == ii.Chapter_title:
                gg += 1
                ii.Num_of_images = int(gg)
            if kk.Content_type == 'Video' and kk.Course_chapter_name == ii.Chapter_title:
                ggw += 1
                ii.Num_of_videos = int(ggw)
            if kk.Content_type == 'Text' and kk.Course_chapter_name == ii.Chapter_title:
                ggy += 1
                ii.Num_of_paragraphs = int(ggy)
        ii.save()
    return render(request, 'chap_tr.html', {'dd': dd,'dm':dm})

def chapter_ad(request):
    gt = Teacher_registration.objects.all()
    dm = Subject.objects.all()
    dd = Course_chapter.objects.all()
    gm = []
    gk = []
    gs = []
    for b in gt:
        for p in dm:
            for v in dd:
                if p.Teacher_id == b.Log_id and v.Sub_id == p.id:
                    if b.Email not in gm:
                        gm.append(b.First_name)
                        gk.append(b.Last_name)
                        gs.append(b.Email)
    dw = []
    dw1 = []
    dw2 = []
    dw3 = []
    dw4 = []
    dw5 = []
    dw6 = []
    rp = []
    for i in dd:
        dw.append(i.Subject_title)
        dw1.append(i.Course_name)
        dw2.append(i.Chapter_title)
        dw3.append(i.Num_of_videos)
        dw4.append(i.Num_of_assignments)
        dw5.append(i.Num_of_images)
        dw6.append(i.Num_of_paragraphs)
        rp.append(i.id)
    tt = zip(dw,dw1,dw2,dw3,dw4,dw5,dw6,gm,gk,gs,rp)
    return render(request, 'chap_ad.html', {'tt': tt})

def edit_chapter1(request, id):
    id = int(id)
    gh = Course_chapter.objects.get(id = id)
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_tt = request.POST.get('c_tt')
        n_s = request.POST.get('n_s')
        vid = request.POST.get('vid')
        imag = request.POST.get('imag')
        prgg = request.POST.get('prgg')
        gh.Subject_title = sub
        gh.Course_name = cou
        gh.Chapter_title = c_tt
        gh.Num_of_assignments = n_s
        if vid != '':
            gh.Num_of_videos  = vid
        if imag != '':
            gh.Num_of_images  = imag
        if prgg != '':
            gh.Num_of_paragraphs  = prgg
        gh.save()

        gt = Teacher_registration.objects.all()
        dm = Subject.objects.all()
        dd = Course_chapter.objects.all()
        gm = []
        gk = []
        gs = []
        for b in gt:
            for p in dm:
                for v in dd:
                    if p.Teacher_id == b.Log_id and v.Sub_id == p.id:
                        if b.Email not in gm:
                            gm.append(b.First_name)
                            gk.append(b.Last_name)
                            gs.append(b.Email)
        dw = []
        dw1 = []
        dw2 = []
        dw3 = []
        dw4 = []
        dw5 = []
        dw6 = []
        rp = []
        for i in dd:
            dw.append(i.Subject_title)
            dw1.append(i.Course_name)
            dw2.append(i.Chapter_title)
            dw3.append(i.Num_of_videos)
            dw4.append(i.Num_of_assignments)
            dw5.append(i.Num_of_images)
            dw6.append(i.Num_of_paragraphs)
            rp.append(i.id)
        tt = zip(dw, dw1, dw2, dw3, dw4, dw5, dw6, gm, gk, gs, rp)
        messages.success(request, 'Chapter edited successfully')
        return render(request, 'chap_ad.html', {'tt': tt})
    return render(request,'edit_chapter1.html',{'gh':gh})

def edit_chapter(request, id):
    dm = Subject.objects.filter(Teacher_id = request.session['logg'])
    gh = Course_chapter.objects.get(id = id)
    dd = Course_chapter.objects.all()
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_tt = request.POST.get('c_tt')
        n_s = request.POST.get('n_s')
        vid = request.POST.get('vid')
        imag = request.POST.get('imag')
        prgg = request.POST.get('prgg')
        gh.Subject_title = sub
        gh.Course_name = cou
        gh.Chapter_title = c_tt
        gh.Num_of_assignments = n_s
        if vid != '':
            gh.Num_of_videos  = vid
        if imag != '':
            gh.Num_of_images  = imag
        if prgg != '':
            gh.Num_of_paragraphs  = prgg
        gh.save()
        messages.success(request, 'Chapter edited successfully')
        return render(request, 'chap_tr.html',{'dd':dd,'dm':dm})
    return render(request,'edit_chapter.html',{'gh':gh})

def delete_chapter1(request, id):
    id = int(id)
    Course_chapter.objects.get(id = id).delete()
    gt = Teacher_registration.objects.all()
    dm = Subject.objects.all()
    dd = Course_chapter.objects.all()
    gm = []
    gk = []
    gs = []
    for b in gt:
        for p in dm:
            for v in dd:
                if p.Teacher_id == b.Log_id and v.Sub_id == p.id:
                    if b.Email not in gm:
                        gm.append(b.First_name)
                        gk.append(b.Last_name)
                        gs.append(b.Email)
    dw = []
    dw1 = []
    dw2 = []
    dw3 = []
    dw4 = []
    dw5 = []
    dw6 = []
    rp = []
    for i in dd:
        dw.append(i.Subject_title)
        dw1.append(i.Course_name)
        dw2.append(i.Chapter_title)
        dw3.append(i.Num_of_videos)
        dw4.append(i.Num_of_assignments)
        dw5.append(i.Num_of_images)
        dw6.append(i.Num_of_paragraphs)
        rp.append(i.id)
    tt = zip(dw, dw1, dw2, dw3, dw4, dw5, dw6, gm, gk, gs, rp)
    messages.success(request, 'Chapter deleted successfully')
    return render(request, 'chap_ad.html', {'tt': tt})

def delete_chapter(request, id):
    Course_chapter.objects.get(id = id).delete()
    dm = Subject.objects.filter(Teacher_id=request.session['logg'])
    dd = Course_chapter.objects.all()
    messages.success(request, 'Chapter deleted successfully')
    return render(request, 'chap_tr.html',{'dd':dd,'dm':dm})

def add_chapter(request):
    dm = Subject.objects.filter(Teacher_id = request.session['logg'])
    dd = Course_chapter.objects.all()
    kk = []
    for i in dm:
        if i.Subject_title not in kk:
            kk.append(i.Subject_title)
    if request.method == 'POST':
        cou_tit = request.POST.get('cou_tit1')
        try:
            ss = Subject.objects.get(Subject_title = request.session['subj_n'], Course_title = cou_tit)
        except:
            messages.success(request, 'Please select subject and course')
            return render(request,'add_chapter.html',{'kk':kk})
        sub_tit = request.session['subj_n']
        ch_tit1 = request.POST.get('ch_tit1')
        assi = request.POST.get('assi')
        vdd = request.POST.get('vdd')
        im = request.POST.get('im')
        parg = request.POST.get('parg')
        cdt = Course_chapter()
        cdt.Subject_title = sub_tit
        cdt.Course_name = cou_tit
        cdt.Chapter_title  = ch_tit1
        cdt.Num_of_assignments = assi
        cdt.Num_of_videos = vdd
        cdt.Num_of_images = im
        cdt.Num_of_paragraphs = parg
        cdt.Sub_id = ss.id
        cdt.save()
        messages.success(request, 'Chapter added successfully')
        return render(request, 'chap_tr.html', {'dd': dd,'dm':dm})
    return render(request,'add_chapter.html',{'kk':kk})

def add_chapter1(request):
   gg = request.POST.get('subj')
   gg1 = Subject.objects.filter(Subject_title = gg, Teacher_id = request.session['logg'])
   request.session['subj_n'] = gg
   return render(request,'add_chapter2.html',{'gg1':gg1})

def ch_co_tr(request):
    mm = Login.objects.get(id = request.session['logg'])
    mm1 = Subject.objects.filter(Teacher_id = mm)
    mm2 = Course_chapter.objects.all()
    nbn = []
    for i in mm1:
        for j in mm2:
            if j.Sub_id == i.id:
                nbn.append(j.id)
    dd = Course_chapter_content.objects.all()
    return render(request, 'cont_tr.html', {'dd': dd,'nbn':nbn})

def ch_co_ad(request):
    gt = Teacher_registration.objects.all()
    dm = Subject.objects.all()
    dd = Course_chapter.objects.all()
    ds = Course_chapter_content.objects.all()
    return render(request, 'cont_ad.html', {'ds': ds,'gt':gt,'dm':dm,'dd':dd})

def edit_content1(request, id):
    gh1 = Course_chapter_content.objects.get(id=id)
    gt = Teacher_registration.objects.all()
    dm = Subject.objects.all()
    dd = Course_chapter.objects.all()
    ds = Course_chapter_content.objects.all()
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_n1 = request.POST.get('c_n')
        s = request.POST.get('s')
        time = request.POST.get('time')
        s1 = request.POST.get('s1')
        cont_typ = request.POST.get('cont_typ')
        gh1.Subject_title = sub
        gh1.Course_name = cou
        gh1.Course_chapter_name = c_n1
        if cont_typ == 1:
            gh1.Content_type = 'Image'
        if cont_typ == 2:
            gh1.Content_type = 'Text'
        if cont_typ == 3:
            gh1.Content_type = 'Video'
        gh1.Is_mandatory  = s
        gh1.Time_required_in_sec  = time
        gh1.Is_open_for_free  = s1
        gh1.save()
        messages.success(request, 'Chapter content edited successfully')
        return render(request, 'cont_ad.html', {'ds': ds,'gt':gt,'dm':dm,'dd':dd})
    return render(request, 'edit_content1.html', {'gh1': gh1})

def edit_content(request, id):
    mm = Login.objects.get(id=request.session['logg'])
    mm1 = Subject.objects.filter(Teacher_id = mm)
    mm2 = Course_chapter.objects.all()
    nbn = []
    for i in mm1:
        for j in mm2:
            if j.Sub_id == i.id:
                nbn.append(j.id)
    dd = Course_chapter_content.objects.all()
    gh = Course_chapter_content.objects.get(id=id)
    if request.method == 'POST':
        sub = request.POST.get('sub')
        cou = request.POST.get('cou')
        c_n1 = request.POST.get('c_n')
        s = request.POST.get('s')
        time = request.POST.get('time')
        s1 = request.POST.get('s1')
        cont_typ = request.POST.get('cont_typ')
        gh.Subject_title = sub
        gh.Course_name = cou
        gh.Course_chapter_name = c_n1
        if int(cont_typ) == 1:
            gh.Content_type = 'Image'
        if int(cont_typ) == 2:
            gh.Content_type = 'Text'
        if int(cont_typ) == 3:
            gh.Content_type = 'Video'
        gh.Is_mandatory  = s
        gh.Time_required_in_sec  = time
        gh.Is_open_for_free  = s1
        gh.save()
        messages.success(request, 'Chapter content edited successfully')
        return render(request, 'cont_tr.html', {'dd': dd,'nbn':nbn})
    return render(request, 'edit_content.html', {'gh': gh})

def delete_content(request, id):
    mm = Login.objects.get(id=request.session['logg'])
    mm1 = Subject.objects.filter(Teacher_id=mm)
    mm2 = Course_chapter.objects.all()
    nbn = []
    for i in mm1:
        for j in mm2:
            if j.Sub_id == i.id:
                nbn.append(j.id)
    Course_chapter_content.objects.get(id = id).delete()
    dd = Course_chapter_content.objects.all()
    messages.success(request, 'Chapter content deleted successfully')
    return render(request, 'cont_tr.html',{'dd':dd,'nbn':nbn})

def add_ch_con(request):
    mm = Login.objects.get(id = request.session['logg'])
    mm1 = Subject.objects.filter(Teacher_id=mm)
    mm2 = Course_chapter.objects.all()
    nbn = []
    for i in mm1:
        for j in mm2:
            if j.Sub_id == i.id:
                nbn.append(j.id)
    dd = Course_chapter_content.objects.all()
    kk = Subject.objects.filter(Teacher_id = request.session['logg'])
    if request.method == 'POST':
        sub_tit = request.session['subj_nn']
        sel_c = request.POST.get('sel_c')
        tex_con = request.POST.get('tex_con')
        fg = Subject.objects.get(id = sel_c)
        ch_tit1 = request.POST.get('ch_tit1')
        try:
            dtb = Course_chapter.objects.get(Sub = sel_c, Chapter_title = ch_tit1)
        except:
            mm = Login.objects.get(id=request.session['logg'])
            mm1 = Subject.objects.filter(Teacher_id=mm)
            mm2 = Course_chapter.objects.all()
            nbn = []
            for i in mm1:
                for j in mm2:
                    if j.Sub_id == i.id:
                        nbn.append(j.id)
            dd = Course_chapter_content.objects.all()
            messages.success(request, 'Please select an existing chapter title')
            return render(request, 'cont_tr.html', {'dd': dd, 'nbn': nbn})
        up_c = request.FILES['up_c']
        fs = FileSystemStorage()
        fs.save(up_c.name, up_c)
        s1 = request.POST.get('s1')
        s = request.POST.get('s')
        cont_typ = request.POST.get('cont_typ')
        cdt = Course_chapter_content()
        cv = int(cont_typ)
        if cv == 1:
            cdt.Content_type = 'Image'
        if cv == 2:
            cdt.Content_type = 'Text'
        if cv == 3:
            cdt.Content_type = 'Video'
        time = request.POST.get('time')
        cdt.Subject_title = sub_tit
        cdt.Course_name = fg.Course_title
        cdt.Course_chapter_name  = ch_tit1
        cdt.Content_name  = up_c
        cdt.Text_content = tex_con
        cdt.Is_mandatory = s
        cdt.Time_required_in_sec = time
        cdt.Is_open_for_free = s1
        cdt.Chapt = dtb
        cdt.save()
        messages.success(request, 'Chapter content added successfully')
        return render(request, 'cont_tr.html', {'dd': dd,'nbn':nbn})
    return render(request,'add_chapter_content.html',{'kk':kk})

def add_chapter_c1(request):
    gg = request.POST.get('subj')
    bb = Subject.objects.filter(Teacher_id = request.session['logg'], Subject_title = gg)
    c = 0
    for i in bb:
        c = i.id
        c = int(c)
        break
    kkm = Course_chapter.objects.filter(Subject_title = gg, Sub = c)
    request.session['subj_nn'] = gg
    return render(request, 'add_chapter_c2.html', {'gg': gg,'bb':bb,'kkm':kkm})

def subject_tr1(request):
    dd = Subject_details.objects.all()
    ft = []
    for j in dd:
        if j.sub_name in ft:
            continue
        ft.append(j.sub_name)
    bb = Registration.objects.get(logi=request.session['logi_id'])
    hj = request.session['topic_name'] = request.POST.get('select')
    ddt = Subject_details.objects.get(sub_topic = hj)
    return render(request, 'sub_tr.html', {'dd': ft, 'bb': bb,'ddt':ddt})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        t_a = request.POST.get('t_a')
        g = Guest_contact()
        g.Contact_email = email
        g.Contact_message = t_a
        g.Contact_name = name
        g.save()
        messages.success(request, 'Message sent successfully')
        return render(request,'home.html')
    return render(request,'contact.html')

def g_m(request):
    bb = Guest_contact.objects.all()
    return render(request,'guest_message.html',{'bb':bb})

def teacher_top(request):
    if request.method == 'POST':
         name = request.session['teacher_name']
         topic = request.session['topic_name']
         email = request.session['teacher_email']
         sub = request.session['subject_name']
         date1 = request.POST.get('date1')
         tcher = Teacher()
         tcher.teacher_name = name
         tcher.teacher_topic = topic
         tcher.teacher_subject = sub
         tcher.teacher_email = email
         tcher.teacher_date =  date1
         tcher.save()
         return render(request,'teacher_home.html')
    return render(request, 'teacher_home.html')

def st_sub_sel(request):
    ss = Teacher.objects.all()
    days = Subject_details.objects.all()
    return render(request, 'student_sub_sel.html', {'ss':ss,'days':days})

def student_book(request):
    if request.method == 'POST':
        tr_name = request.session['teac_name']
        tr_sub = request.session['teacher_sub']
        tr_topic = request.session['sub_topic']
        tr_start_date =  request.session['teac_date']
        tr_dr = request.POST.get('select')
        buk = Student_book()
        buk.teacher_name = tr_name
        buk.teacher_subject = tr_sub
        buk.teacher_topic = tr_topic
        buk.starting_date = tr_start_date
        buk.topic_dr = tr_dr
        buk.save()
        return render(request, 'student_home.html')
    return render(request, 'student_home.html')

def teacher_book(request):
    book = Teacher.objects.all()
    return render(request, 'teacher_sub_sel.html', {'book': book})

def adm_prof(request):
    gtt = Login.objects.filter(User_role='admin')
    gtt1 = Admin_registration.objects.all()
    return render(request, 'adm_prof.html',{'gtt':gtt,'gtt1':gtt1})

def del_admin(request, id):
    Login.objects.get(id = id).delete()
    messages.success(request, 'You have successfully resigned from administration')
    return render(request, 'home.html')

def delete_g_msg(request,id):
    Guest_contact.objects.get(id=id).delete()
    bb = Guest_contact.objects.all()
    messages.success(request, 'Message deleted successfully')
    return render(request, 'guest_message.html',{'bb':bb})

def edit_admin(request):
    bb1 = Admin_registration.objects.all()
    return render(request, 'update_admin.html',{'bb1':bb1})

def bnb(request):
    if request.method == 'POST':
        first = request.POST.get('first')
        last = request.POST.get('last')
        em = request.POST.get('em')
        psw = request.POST.get('psw')
        dcd = Login.objects.get(User_role = 'admin')
        dcd.Email = em
        dcd.Password = psw
        dcd.save()
        dcd1 = Admin_registration.objects.get(Log_id = request.session['logg'])
        dcd1.First_name = first
        dcd1.Last_name = last
        dcd1.Email = em
        dcd1.Password = psw
        dcd1.save()
        ss = Student_registration.objects.all()
        tt = Teacher_registration.objects.all()
        messages.success(request, 'You have successfully updated your profile')
        return render(request, "admin_home.html", {'ss': ss, 'tt': tt})
    else:
        ss = Student_registration.objects.all()
        tt = Teacher_registration.objects.all()
        return render(request, "admin_home.html", {'ss': ss, 'tt': tt})

def stu_sub_selnew(request):
    sne = Subject.objects.all()
    snew = []
    for i in sne:
        if i.Subject_title not in snew:
            snew.append(i.Subject_title)
    return render(request, 'st_sub_selnew1.html',{'snew':snew})

def st_sub_selnew2(request):
    d = request.POST.get('subj')
    request.session['sub_n'] = d
    snew1 = Subject.objects.filter(Subject_title = d)
    return render(request, 'st_sub_selnew2.html', {'snew1': snew1})

def disp_teach(request):
    couu = request.POST.get('cou')
    request.session['course'] = couu
    drt = Subject.objects.filter(Subject_title = request.session['sub_n'], Course_title = couu)
    gh = Teacher_registration.objects.all()
    return render(request,'st_sub_selnew.html',{'drt':drt,'gh':gh})
def stu_buk_teacherr(request, id):
    request.session['paid'] = id
    return render(request,'paid.html')
def stu_buk_teacher(request):
    paidd = request.POST.get('paid')
    dh = Student_registration.objects.get(Log_id = request.session['logg'])
    nm = Teacher_registration.objects.get(id = request.session['paid'])
    gg = Subject.objects.get(Teacher_id = nm.Log_id,Course_title = request.session['course'], Subject_title = request.session['sub_n'])
    spp = Enrollment()
    spp.Student_name = dh.First_name
    spp.Student_email = dh.Email
    spp.Subject_name = request.session['sub_n']
    spp.Course_name = request.session['course']
    spp.Teacher_name = nm.First_name
    spp.Teacher_email = nm.Email
    if int(gg.Course_fee) > int(paidd):
        messages.success(request, 'Please pay full amount')
        return render(request,'paid.html')
    spp.Paid_amount = paidd
    spp.Attendance = 0
    spp.Pending_days = 0
    spp.Teacher_response = 'To be expected'
    if gg.Course_fee > 0:
        spp.Is_paid_subscription = 'True'
    else:
        spp.Is_paid_subscription = 'False'
    spp.save()
    messages.success(request, 'You have successfully booked a course')
    return render(request,'student_home.html')

def upl_cer(request):
    ss = Student_registration.objects.all()
    if request.method == 'POST':
        try:
            cert = request.FILES['cert']
            fs = FileSystemStorage()
            fs.save(cert.name,cert)
            stu_id = request.POST.get('stu_id')
            try:
                djk = Student_registration.objects.get(id = stu_id)
            except:
                messages.success(request, 'Please select a student')
                return render(request,'upload_cert.html',{'ss':ss})
            cc = Certificates()
            cc.Student_name = djk.First_name
            cc.Student_email = djk.Email
            cc.Certificate = cert
            cc.save()
            ss = Student_registration.objects.all()
            tt = Teacher_registration.objects.all()
            messages.success(request, 'Certificate uploaded successfully')
            return render(request, "admin_home.html", {'ss': ss, 'tt': tt})
        except:
            cert = request.POST.get('cert')
            stu_id = request.POST.get('stu_id')
            djk = Student_registration.objects.get(id = stu_id)
            cc = Certificates()
            cc.Student_name = djk.First_name
            cc.Student_email = djk.Email
            cc.Certificate = cert
            cc.save()
            ss = Student_registration.objects.all()
            tt = Teacher_registration.objects.all()
            messages.success(request, 'Certificate uploaded successfully')
            return render(request, "admin_home.html", {'ss': ss, 'tt': tt})
    return render(request,'upload_cert.html',{'ss':ss})

def del_cer(request):
    df = Certificates.objects.all()
    return render(request,'del_cer.html',{'df':df})

def delete_cert(request, id):
    Certificates.objects.get(id = id).delete()
    df = Certificates.objects.all()
    messages.success(request, 'Deleted certificate')
    return render(request, 'del_cer.html', {'df': df})

def do_cer(request):
    dd = Student_registration.objects.get(Log_id = request.session['logg'])
    try:
        sr = Certificates.objects.filter(Student_name = dd.First_name, Student_email = dd.Email)
    except:
        messages.success(request, 'No certificate available')
        return render(request, 'student_home.html')
    return render(request,'do_cer.html',{'sr':sr})

def m_m(request):
    p = Login.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    return render(request,'message.html',{'bb':bb})

def del_msg_admin(request,id):
    Messages.objects.get(id = id).delete()
    p = Login.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    messages.success(request, 'Message deleted successfully')
    return render(request,'message.html',{'bb':bb})

def reply_msg_admin(request,id):
    pa = Messages.objects.get(id = id)
    p = Login.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    if request.method == 'POST':
        f_email = request.POST.get('f_email')
        to_email = request.POST.get('to_email')
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Category = p.User_role
        pa1.From_email = to_email
        pa1.To_email = f_email
        pa1.Message_content = msg_cont
        pa1.save()
        messages.success(request, 'Message reply successful')
        return render(request, 'message.html', {'bb': bb})
    return render(request,'reply_msg_admin.html',{'pa':pa})

def sent_msg_admin(request):
    kk = Login.objects.all()
    p = Login.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = str(to_em)
        gg = ddp.split()
        pnm = gg[0]
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Category = p.User_role
        kkp = Login.objects.get(id = request.session['logg'])
        nm.From_email = kkp.Email
        nm.To_email = pnm
        nm.Message_content = msg_cont
        nm.save()
        messages.success(request, 'Message sent successfully')
        return render(request, 'message.html', {'bb': bb})
    return render(request,'sent_msg_admin.html',{'kk':kk})


def subj_display(request):
    cd = Subject.objects.all()
    return render(request,'subj_display.html')

def m_m1(request):
    p = Login.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    return render(request,'message1.html',{'bb':bb})

def del_msg_teacher(request,id):
    Messages.objects.get(id = id).delete()
    p = Login.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    messages.success(request, 'Message deleted successfully')
    return render(request,'message1.html',{'bb':bb})

def reply_msg_teacher(request,id):
    pa = Messages.objects.get(id = id)
    p = Login.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    if request.method == 'POST':
        f_email = request.POST.get('f_email')
        to_email = request.POST.get('to_email')
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Category = p.User_role
        pa1.From_email = to_email
        pa1.To_email = f_email
        pa1.Message_content = msg_cont
        pa1.save()
        messages.success(request, 'Message reply successful')
        return render(request, 'message1.html', {'bb': bb})
    return render(request,'reply_msg_teacher1.html',{'pa':pa})

def sent_msg_teacher(request):
    kk = Login.objects.all()
    p = Login.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = str(to_em)
        gg = ddp.split()
        pnm = gg[0]
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Category = p.User_role
        kkp = Login.objects.get(id = request.session['logg'])
        nm.From_email = kkp.Email
        nm.To_email = pnm
        nm.Message_content = msg_cont
        nm.save()
        messages.success(request, 'Message sent successfully')
        return render(request, 'message1.html', {'bb': bb})
    return render(request,'sent_msg_teacher.html',{'kk':kk})



def m_m2(request):
    p = Login.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_email = p.Email)
    return render(request,'message2.html',{'bb':bb})

def del_msg_student(request,id):
    Messages.objects.get(id = id).delete()
    p = Login.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    messages.success(request, 'Message deleted successfully')
    return render(request,'message2.html',{'bb':bb})

def reply_msg_student(request,id):
    pa = Messages.objects.get(id = id)
    p = Login.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    if request.method == 'POST':
        f_email = request.POST.get('f_email')
        to_email = request.POST.get('to_email')
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Category = p.User_role
        pa1.From_email = to_email
        pa1.To_email = f_email
        pa1.Message_content = msg_cont
        pa1.save()
        messages.success(request, 'Message reply successful')
        return render(request, 'message2.html', {'bb': bb})
    return render(request,'reply_msg_student.html',{'pa':pa})

def sent_msg_student(request):
    kk = Login.objects.all()
    p = Login.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_email=p.Email)
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = str(to_em)
        gg = ddp.split()
        pnm = gg[0]
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Category = p.User_role
        kkp = Login.objects.get(id = request.session['logg'])
        nm.From_email = kkp.Email
        nm.To_email = pnm
        nm.Message_content = msg_cont
        nm.save()
        messages.success(request, 'Message sent successfully')
        return render(request, 'message2.html', {'bb': bb})
    return render(request,'sent_msg_student.html',{'kk':kk})



def msg_student(request):
    if request.method == "POST":
        femail = request.POST.get('femail')
        email= request.POST.get('email')
        bb = Registration.objects.get(email=email)
        subject= request.POST.get('subject')
        msg=Message()
        msg.name=femail
        msg.email = email
        msg.rec_name = bb.user_category
        msg.msg=subject
        msg.save()
    return render(request, 'student_home.html')


def msg_teacher(request):
    if request.method == "POST":
        femail = request.POST.get('femail')
        email= request.POST.get('email')
        bb = Registration.objects.get(email=email)
        subject= request.POST.get('subject')
        msg=Message()
        msg.name=femail
        msg.email = email
        msg.rec_name = bb.user_category
        msg.msg=subject
        msg.save()
    return render(request, 'teacher_home.html')

def st_book_courses(request):
    st = Student_registration.objects.get(Log_id = request.session['logg'])
    buk = Enrollment.objects.filter(Student_email = st.Email)
    return render(request, 'st_book_courses.html',{'buk':buk,'st':st})

def acc_chapter(request, id):
    gh = Enrollment.objects.get(id=id)
    if gh.Teacher_response == 'To be expected':
        messages.success(request, 'Please wait for approval')
        return render(request, 'student_home.html')
    if gh.Teacher_response == 'Rejected':
        messages.success(request, 'You are not allowed to access course contents')
        return render(request, 'student_home.html')
    dd = Course_chapter.objects.filter(Course_name = gh.Course_name)
    nn = Login.objects.get(Email = gh.Teacher_email)
    dm = Subject.objects.get(Subject_title = gh.Subject_name, Course_title = gh.Course_name, Teacher_id = nn.id)
    if dm.Course_fee > gh.Paid_amount:
        messages.success(request, 'Your payment balance is pending')
        return render(request, 'student_home.html')
    fd = []
    for i in dd:
        if i.Chapter_title not in fd:
            fd.append(i.Chapter_title)
    return render(request, 'acc_chapter1.html', {'fd':fd})

def acc_chapter1(request):
    sz1 = request.POST.get('cha')
    dsw = Student_registration.objects.get(Log_id = request.session["logg"])
    ksk = Learning_progress.objects.filter(Course_chapter_name = sz1, Student_email = dsw.Email)
    for y in ksk:
        if y.Status == "C":
            messages.success(request, 'You have already finished this chapter')
            return render(request, 'student_home.html')
    sz = Course_chapter_content.objects.filter(Course_chapter_name = sz1)
    return render(request,'acc_chapter2.html',{'sz':sz})
def compp(request):
    mbm = Login.objects.get(id = request.session['logg'])
    mnm = Student_registration.objects.get(Log_id = mbm)
    idd = request.POST.getlist('id')
    comm = request.POST.get('comm')
    for i in idd:
       df = Course_chapter_content.objects.get(id = i)
       try:
           pk = Learning_progress.objects.get(Student_name = mnm.First_name, Student_email = mnm.Email, Subject_name = df.Subject_title, Course_name = df.Course_name, Course_chapter_content_name = df.Content_name, Course_chapter_name = df.Course_chapter_name)
           pk.Student_name = mnm.First_name
           pk.Student_email = mnm.Email
           pk.Subject_name = df.Subject_title
           pk.Course_name = df.Course_name
           pk.Course_chapter_name = df.Course_chapter_name
           pk.Course_chapter_content_name = df.Content_name
           pk.Status = comm
           pk.save()
       except:
           pk = Learning_progress()
           pk.Student_name = mnm.First_name
           pk.Student_email = mnm.Email
           pk.Subject_name = df.Subject_title
           pk.Course_name = df.Course_name
           pk.Course_chapter_name = df.Course_chapter_name
           pk.Course_chapter_content_name = df.Content_name
           pk.Status = comm
           pk.save()
    return render(request,'student_home.html')

def st_pr(request):
    vc = Login.objects.get(id = request.session['logg'])
    hgh1 = Enrollment.objects.filter(Teacher_email = vc.Email)
    hgh = []
    for i in hgh1:
        if i.Student_email not in hgh:
            hgh.append(i.Student_email)
    dd = Learning_progress.objects.all()
    return render(request,'student_progress.html',{'dd':dd,'hgh':hgh})

def delete_learn_progress(request, id):
    Learning_progress.objects.get(id = id).delete()
    vc = Login.objects.get(id=request.session['logg'])
    hgh1 = Enrollment.objects.filter(Teacher_email=vc.Email)
    hgh = []
    for i in hgh1:
        if i.Student_email not in hgh:
            hgh.append(i.Student_email)
    dd = Learning_progress.objects.all()
    return render(request, 'student_progress.html', {'dd': dd, 'hgh': hgh})

def atten(request):
    h = Login.objects.get(id = request.session['logg'])
    ss = Enrollment.objects.filter(Teacher_email = h.Email)
    if request.method == 'POST':
        atn = request.POST.get('atn')
        atn1 = request.POST.get('atn1')
        dw = Enrollment.objects.get(id = atn)
        dw.Attendance = atn1
        dw.save()
        messages.success(request, 'Attendance given')
        return render(request, 'teacher_home.html')
    return render(request,'atten.html',{'ss':ss})


def msgg_admin(request):
    ddd=Message.objects.all()
    return render(request, 'ad_message.html', {'ddd': ddd})

def msgg_student(request):
    bb = Messages.objects.filter(name=request.session['email'])
    bbx=Message.objects.filter(email=request.session['email'])

    return render(request, 'student_messages.html', {'bb': bb,'bbx':bbx})

def start_test(request):
    hh = Login.objects.get(id=request.session['logg'])
    fg = Exam.objects.filter(Student_email=hh.Email)
    x = datetime.datetime.now()
    x = pytz.utc.localize(x)
    fgc = timezone.now()
    hj = []
    for i in fg:
        zz = i.Time_start
        nb = i.Time_stop
        if fgc>zz and fgc<nb:
            nb = Exam.objects.filter(Student_email=hh.Email,Time_start__lte = fgc, Time_stop__gte = fgc)
            for i in nb:
                if i.Lock == 'locked':
                    messages.success(request, 'You have already attended the exam')
                    return render(request, 'student_home.html')
            for i in nb:
                hj.append(i.Correct_answer)
                request.session['teec'] = i.Teacher_name
                request.session['ssub'] = i.Subject_name
                request.session['student'] = i.Student_name
                request.session['student_ema'] = i.Student_email
                local_dt = timezone.localtime(i.Time_stop, pytz.timezone('Asia/Calcutta'))
                local_dt1 = local_dt.strftime("%Y-%m-%d %H:%M:%S")
                gg = str(local_dt1)
            request.session['exam_id'] = hj
            return render(request,'start_test.html',{'nb':nb,'gg':gg})
    messages.success(request, 'No exam is scheduled now')
    return render(request, 'student_home.html')

def save_exam(request):
    end_time = request.POST.get('end_time')
    endd = end_time[0:19]
    edr = datetime.datetime.strptime(endd, '%Y-%m-%d %H:%M:%S')
    b = datetime.datetime.now()
    bb = b.strftime('%Y-%m-%d %H:%M:%S')
    edr1 = datetime.datetime.strptime(bb, '%Y-%m-%d %H:%M:%S')
    if edr1 > edr:
        messages.success(request, 'You have timed out')
        return render(request, 'student_home.html')
    correct_answers = request.POST.getlist('exx3')
    answers = request.POST.getlist('exx')
    if len(correct_answers) != len(answers):
        messages.success(request, 'Your exam attempt failed due to selecting multiple answers')
        return render(request,'student_home.html')
    count = 0
    count1 = 0
    for i in correct_answers:
        count1 += 1
    for i,j in zip(correct_answers,answers):
        if i == j:
            count += 1
    hh = Login.objects.get(id=request.session['logg'])
    fg = Exam.objects.filter(Student_email = hh.Email)
    x = datetime.datetime.now()
    x = pytz.utc.localize(x)
    fgc = timezone.now()
    for i in fg:
        zz = i.Time_start
        nb = i.Time_stop
        if fgc > zz and fgc < nb:
            nb = Exam.objects.filter(Student_email=hh.Email, Time_start__lte = fgc, Time_stop__gte = fgc)
            for i in nb:
                i.Lock = 'locked'
                i.save()
    ddd = Exam_results()
    ddd.Student_name = request.session['student']
    ddd.Student_email = request.session['student_ema']
    ddd.Teacher_name = request.session['teec']
    ddd.Teacher_email = request.session['teec']
    ddd.Subject_name = request.session['ssub']
    ddd.Total_marks = count1
    ddd.Acquired_marks = count
    avg = 100 * float(count)/float(count1)
    if avg >= 80:
        ddd.Grade = 'A'
    elif avg < 80 and avg >= 50 :
        ddd.Grade = 'B'
    elif avg < 50 and avg >= 30:
        ddd.Grade = 'C'
    else:
        ddd.Grade = 'Failed'
    ddd.Time_stop = b
    ddd.save()
    messages.success(request, 'You have successfully finished your exam')
    return render(request, 'student_home.html')

def exam_result(request):
    gt = Exam_results.objects.all()
    hh = Teacher_registration.objects.get(Log_id=request.session['logg'])
    return render(request,'exam_result.html',{'hh':hh,'gt':gt})

def exam_result1(request):
    gt = Exam_results.objects.all()
    hh = Student_registration.objects.get(Log_id = request.session['logg'])
    return render(request,'exam_result1.html',{'hh':hh,'gt':gt})

def delete_ex_re(request, id):
    Exam_results.objects.get(id=id).delete()
    gt = Exam_results.objects.all()
    hh = Teacher_registration.objects.get(Log_id=request.session['logg'])
    return render(request, 'exam_result.html', {'hh': hh, 'gt': gt})

def delete_test(request):
    hh = Teacher_registration.objects.get(Log_id=request.session['logg'])
    fg = Exam.objects.filter(Teacher_name = hh.First_name)
    return render(request, 'delete_test.html', {'fg': fg})

def delete_test1(request, id):
    Exam.objects.get(id = id).delete()
    hh = Teacher_registration.objects.get(Log_id=request.session['logg'])
    fg = Exam.objects.filter(Teacher_name=hh.First_name)
    return render(request, 'delete_test.html', {'fg': fg})

def block(request):
    t_reg = Teacher_registration.objects.all()
    s_reg = Student_registration.objects.all()
    kkm = Login.objects.all()
    return render(request,'block.html',{'t_reg':t_reg,'s_reg':s_reg,'kkm':kkm})

def blocks(request, id):
    klk = Teacher_registration.objects.get(id=id)
    hyh = Login.objects.get(Email = klk.Email)
    hyh.User_role = 'Blocked'
    hyh.save()
    t_reg = Teacher_registration.objects.all()
    s_reg = Student_registration.objects.all()
    kkm = Login.objects.all()
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg, 'kkm':kkm})

def blocks1(request, id):
    klk = Student_registration.objects.get(id=id)
    hyh = Login.objects.get(Email=klk.Email)
    hyh.User_role = 'Blocked'
    hyh.save()
    t_reg = Teacher_registration.objects.all()
    s_reg = Student_registration.objects.all()
    kkm = Login.objects.all()
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg,'kkm':kkm})

def allows(request, id):
    klk = Teacher_registration.objects.get(id=id)
    hyh = Login.objects.get(Email=klk.Email)
    hyh.User_role = 'teacher'
    hyh.save()
    t_reg = Teacher_registration.objects.all()
    s_reg = Student_registration.objects.all()
    kkm = Login.objects.all()
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg,'kkm':kkm})

def allows1(request, id):
    klk = Student_registration.objects.get(id=id)
    hyh = Login.objects.get(Email=klk.Email)
    hyh.User_role = 'student'
    hyh.save()
    t_reg = Teacher_registration.objects.all()
    s_reg = Student_registration.objects.all()
    kkm = Login.objects.all()
    return render(request, 'block.html', {'t_reg': t_reg, 's_reg': s_reg,'kkm':kkm})

def feedback(request):
    x = datetime.datetime.now()
    y = x.strftime("%Y-%m-%d")
    dd = Login.objects.get(id = request.session['logg'])
    ds = Enrollment.objects.filter(Student_email = dd.Email)
    fd = []
    fdd = []
    fdm = zip(fdd,fd)
    for i in ds:
        if i.Course_name not in fd:
            fd.append(i.Course_name)
            fdd.append(i.id)
    fd1 = []
    fdd1 = []
    fddm = zip(fdd1,fd1)
    for i in ds:
        if i.Subject_name not in fd1:
            fd1.append(i.Subject_name)
            fdd1.append(i.id)
    if request.method == 'POST':
        course1 = request.POST.get('select')
        subject1 = request.POST.get('select3')
        if str(course1) == 'nil' or str(subject1) == 'nil':
            messages.success(request, 'Please fill all fields')
            return render(request,'feedback.html',{'fdm':fdm,'fddm':fddm})
        cdc = Enrollment.objects.get(id = int(course1))
        course = cdc.Course_name
        cdc1 = Enrollment.objects.get(id=int(subject1))
        subject = cdc1.Subject_name
        score = request.POST.get('select1')
        text_feed = request.POST.get('text_feed')
        qw = Feedback()
        qw.Subject_name = subject
        for i in ds:
            qw.Student_name = i.Student_name
            qw.Student_email = i.Student_email
            break
        qw.Course_name = course
        qw.Feedback_text = text_feed
        qw.Rating_score = score
        qw.Submission_date = y
        qw.save()
        messages.success(request, 'Thank you for your valuable feedback')
        return render(request, 'student_home.html')
    return render(request,'feedback.html',{'fdm':fdm,'fddm':fddm})

def feedbak(request):
    se = Feedback.objects.all()
    return render(request,'feedbak.html',{'se':se})

def delete_feedback(request, id):
    Feedback.objects.get(id=id).delete()
    se = Feedback.objects.all()
    return render(request, 'feedbak.html', {'se': se})

def review(request):
    pp = Login.objects.get(id = request.session['logg'])
    tt = Enrollment.objects.filter(Student_email = pp.Email)
    g = []
    for z in tt:
        if z.Teacher_email not in g:
            g.append(z.Teacher_email)
    if request.method == 'POST':
        tea_sel = request.POST.get('select')
        score = request.POST.get('select1')
        dv = Teacher_registration.objects.get(Email = tea_sel)
        hw = Review()
        hw.Review = score
        hw.Teacher = dv
        hw.save()
        hw1 = Review.objects.filter(Teacher = dv)
        bdw = 0
        for p in hw1:
            bdw += 1
        ht = []
        for i in hw1:
            ht.append(i.Review)
        aq = ht.count(1)
        aq1 = ht.count(2)
        aq2 = ht.count(3)
        aq3 = ht.count(4)
        aq4 = ht.count(5)
        br = [aq,aq1,aq2,aq3,aq4]
        brr = max(br)
        for i in br:
            if aq == brr:
                br1 = 1
            if aq1 == brr:
                br1 = 2
            if aq2 == brr:
                br1 = 3
            if aq3 == brr:
                br1 = 4
            if aq4 == brr:
                br1 = 5
        dv.Num_of_reviews = bdw
        dv.Average_review_rating = br1
        dv.save()
        messages.success(request, 'Thank you for your valuable rating')
        return render(request, 'student_home.html')
    return render(request,'review.html',{'g':g})

def delete_review(request):
    revv = Review.objects.all()
    ttt = Teacher_registration.objects.all()
    tn = []
    tn1 = []
    te = []
    ts = []
    td = []
    for i in revv:
        for y in ttt:
            if y == i.Teacher:
                tn.append(y.First_name)
                tn1.append(y.Last_name)
                te.append(y.Email)
                ts.append(i.Review)
                td.append(i.id)
    rev = zip(tn,tn1,te,ts,td)
    return render(request,'del_review.html',{'rev':rev})

def delete_review1(request, id):
    Review.objects.get(id = id).delete()
    revv = Review.objects.all()
    ttt = Teacher_registration.objects.all()
    tn = []
    tn1 = []
    te = []
    ts = []
    td = []
    for i in revv:
        for y in ttt:
            if y == i.Teacher:
                tn.append(y.First_name)
                tn1.append(y.Last_name)
                te.append(y.Email)
                ts.append(i.Review)
                td.append(i.id)
    rev = zip(tn, tn1, te, ts, td)
    return render(request, 'del_review.html', {'rev': rev})


def ch_p(request):
    th = Login.objects.get(id = request.session['logg'])
    tt = Student_registration.objects.get(Log_id = th)
    if request.method == 'POST':
        new_pass = request.POST.get('pssw')
        old_pass = request.POST.get('pssw_old')
        email = request.POST.get('em')
        cate = request.POST.get('usr')
        nam = request.POST.get('nam')
        g = Requests()
        g.Name = nam
        g.Email = email
        g.User_category = cate
        g.Old_password = old_pass
        g.New_password = new_pass
        g.save()
        messages.success(request, 'Please wait for your password approval.. Continue to use old password')
        return render(request, 'student_home.html')
    return render(request,'change_password.html',{'th':th,'tt':tt})

def ch_p11(request):
    th = Login.objects.get(id=request.session['logg'])
    tt = Teacher_registration.objects.get(Log_id=th)
    if request.method == 'POST':
        new_pass = request.POST.get('pssw')
        old_pass = request.POST.get('pssw_old')
        email = request.POST.get('em')
        cate = request.POST.get('usr')
        nam = request.POST.get('nam')
        g = Requests()
        g.Name = nam
        g.Email = email
        g.User_category = cate
        g.Old_password = old_pass
        g.New_password = new_pass
        g.save()
        messages.success(request, 'Please wait for your password approval.. Continue to use old password')
        return render(request, 'Teacher_home.html')
    return render(request, 'change_password1.html', {'th': th, 'tt': tt})

def pass_req(request):
    dd = Requests.objects.all()
    return render(request,'pass_req.html',{'dd':dd})

def pass_req1(request, id):
    ff = Requests.objects.get(id = id)
    tt = Login.objects.get(Email = ff.Email)
    try:
        tty = Student_registration.objects.get(Email = ff.Email)
        tty.Password = ff.New_password
        tty.save()
    except:
        tty = Teacher_registration.objects.get(Email = ff.Email)
        tty.Password = ff.New_password
        tty.save()
    tt.Password = ff.New_password
    tt.save()
    Requests.objects.get(id=id).delete()
    dd = Requests.objects.all()
    return render(request, 'pass_req.html', {'dd': dd})


