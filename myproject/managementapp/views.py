from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from django.urls import reverse
from django.utils import timezone 

#login
def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render({},request))

def login_ok(request):
    email = request.POST['email']
    pwd = request.POST['pwd']

    try:
        member = Member.objects.get(email=email)
    except Member.DoesNotExist:
        member = None

    #2:success, 1:pwd error 0:email non-exist
    result=0
    if member!=None:
        if member.pwd==pwd:
            result=2
            request.session['login_ok_user'] = member.email
            request.session['login_user_name'] = member.name
            request.session['login_user_generation'] = member.generation
        else:
            result=1
    else:
        result=0 

    template = loader.get_template('login_ok.html')
    context = {
        'result': result
    }
    
    return HttpResponse(template.render(context,request))

def logout(request):
    if request.session.get('login_ok_user'):
        del request.session['login_ok_user']

    return redirect('../')

#home
def home(request):
    template = loader.get_template('home.html')
    
    return HttpResponse(template.render({},request))


#notices
def notices(request):
    template = loader.get_template('notices/notices.html')
    documents = Documents.objects.all()
    count = len(documents)
    context = {
        'documents':documents,
        'count': count
    }
    return HttpResponse(template.render(context,request))

def notice_search(request):
    template = loader.get_template('notices/notices.html')

    search = request.GET.get('search','') #기본값 = ''
    print('search:',search)
    if search:
        #title_icontains: 대소문자 구분없이 문자열이 존재하는지 확인
        documents = Documents.objects.filter(title__icontains=search)
    else:
        documents = Documents.objects.all()

    context = {
        'documents':documents
    }

    return HttpResponse(template.render(context,request))

def notice_write(request):
    return render(request, 'notices/notice_write.html')

def notice_write_ok(request):   
    writer = request.session['login_user_name']
    title = request.POST['title']
    content = request.POST['content']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

    document = Documents(title=title, writer=writer, content=content, udate=nowDatetime, rdate=nowDatetime, view_count =0)
    document.save()

    return HttpResponseRedirect(reverse('notices'))

def notice_content(request,id):
    template = loader.get_template('notices/notice_content.html')
    document=Documents.objects.get(id=id)
    document.view_count += 1
    document.save()
    context = {
        'document': document
    }
    
    return HttpResponse(template.render(context,request))
    
def notice_update(request,id):
    template = loader.get_template('notices/notice_update.html')
    document=Documents.objects.get(id=id)
    context = {
        'document': document
    }
    return HttpResponse(template.render(context,request))

def notice_update_ok(request,id):
    title = request.POST['title']
    content = request.POST['content']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    
    document = Documents.objects.get(id=id)
    document.title = title
    document.content = content
    document.udate = nowDatetime
    document.save()
    
    return HttpResponseRedirect(reverse('notices'))


def notice_delete(request,id):
    document = Documents.objects.get(id=id)
    document.delete()

    return HttpResponseRedirect(reverse('notices')) 


#classroom
def classroom(request):
    template = loader.get_template('classroom/classroom.html')
    assignments = Assignments.objects.all()
    count = len(assignments)
    context = {
        'assignments': assignments,
        'count': count
    }
    return HttpResponse(template.render(context,request))

def classroom_search(request):
    template = loader.get_template('classroom/classroom.html')

    search = request.GET.get('search','') #기본값 = ''
    print('search:',search)
    if search:
        #title_icontains: 대소문자 구분없이 문자열이 존재하는지 확인
        assignments = Assignments.objects.filter(title__icontains=search)
    else:
        assignments = Assignments.objects.all()

    context = {
        'assignments':assignments
    }

    return HttpResponse(template.render(context,request))
    
def classroom_write(request):
    return render(request, 'classroom/classroom_write.html')

def classroom_write_ok(request):   
    writer = request.session['login_user_name']
    title = request.POST['title']
    content = request.POST['content']
    deadline = request.POST['deadline']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

    assignment = Assignments(title=title, writer=writer, content=content, udate=nowDatetime, rdate=nowDatetime, deadline=deadline, view_count =0)
    assignment.save()

    return HttpResponseRedirect(reverse('classroom'))

def classroom_content(request,id):
    template = loader.get_template('classroom/classroom_content.html')

    assignment=Assignments.objects.get(id=id)
    assignment.view_count += 1
    assignment.save()
    comments = Comments.objects.filter(assignment=assignment)

    context = {
        'assignment': assignment,
        'comments':comments
    }
    
    return HttpResponse(template.render(context,request))

def classroom_comment(request):
    assignment = requst.POST['assignment']
    author = request.session['login_user_name']
    email = request.session['login_ok_user']
    content = request.POST['content']

    comments = Comments(assignment=assignment, author=author, email=email, content=content)
    comments.save()

    return HttpResponseRedirect(reverse('../'))

def classroom_update(request, id):
    template = loader.get_template('classroom/classroom_update.html')
    assignment=Assignments.objects.get(id=id)
    context = {
        'assignment': assignment
    }
    return HttpResponse(template.render(context,request))

def classroom_update_ok(request, id):
    title = request.POST['title']
    content = request.POST['content']
    deadline = request.POST['deadline']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

    assignment=Assignments.objects.get(id=id)
    assignment.title = title
    assignment.content = content
    assignment.deadline = deadline
    assignment.udate = nowDatetime
    assignment.save()

    return HttpResponseRedirect(reverse('classroom'))

def classroom_delete(request, id):

    assignment = Assignments.objects.get(id=id)
    assignment.delete()

    return HttpResponseRedirect(reverse('classroom')) 

#attendance
def attendance(request):
    template = loader.get_template('attendance/attendance.html')
    notices = AttendanceNotice.objects.all()
    requests = AttendanceRequest.objects.all()
    context = {
        'notices' : notices,
        'requests' : requests
    }
    return HttpResponse(template.render(context,request))

def att_notice_content(request, id):
    template = loader.get_template('attendance/att_notice_content.html')
    notice = AttendanceNotice.objects.get(id=id)
    notice.view_count += 1
    notice.save()

    context = {
        'notice': notice
    }
    return HttpResponse(template.render(context, request))


def att_notice_update(request, id):
    template = loader.get_template('attendance/att_notice_update.html')
    notice = AttendanceNotice.objects.get(id=id)
    context = {
        'notice': notice
    }
    return HttpResponse(template.render(context,request))

def att_notice_update_ok(request,id):
    title = request.POST['title']
    content = request.POST['content']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    
    notice = AttendanceNotice.objects.get(id=id)
    notice.title = title
    notice.content = content
    notice.udate = nowDatetime
    notice.save()
    
    return HttpResponseRedirect(reverse('attendance'))

def att_request_details(request, id):
    template = loader.get_template('attendance/att_request_details.html')
    requests = AttendanceRequest.objects.get(id=id)

    context = {
        'requests': requests
    }
    return HttpResponse(template.render(context, request))

def att_write(request):
    template = loader.get_template('attendance/att_write.html')

    return HttpResponse(template.render({},request))

def att_write_ok(request,id):
    writer = request.session['login_user_name']
    title = '출결 관리 요청'
    content = request.POST['content']
    request_type = request.POST['request_type']
    request_date = request.POST['request_date']
    files = request.POST['files']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

    attendancerequest = AttendanceRequest(writer=writer, title=title, content=content, rdate = nowDatetime,
                                        request_date=request_date, request_type=request_type, files=files)
    attendancerequest.save()

    return HttpResponseRedirect(reverse('attendance'))
