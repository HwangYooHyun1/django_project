from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from django.urls import reverse
import calendar
from django.utils import timezone 
from datetime import date, timedelta
from django.utils.timezone import now
from django.db.models import F, ExpressionWrapper,  DurationField
from django.db.models.functions import TruncDate

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

def join(request):
    template = loader.get_template('join.html')
    return HttpResponse(template.render({},request))

def join_ok(request):
    email_front = request.POST.get('email-front', '').strip()
    email_domain = request.POST.get('email-domain', '').strip()
    email = f"{email_front}@{email_domain}" if email_front and email_domain else None
    name = request.POST['name']
    pwd = request.POST['pwd']
    generation = request.POST['generation']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    
    member = Member(name=name, email=email, pwd=pwd, generation=generation, rdate=nowDatetime, udate=nowDatetime)
    member.save()

    return HttpResponseRedirect(reverse('login'))

#home
def home(request):
    template = loader.get_template('home.html')

    # 공지사항 공지일 상위 3개 
    documents = Documents.objects.all().order_by('-udate')[:3]

    #클래스룸 마감일 상위 3개 
    today = now().date()  # 현재 날짜

    classroom = Assignments.objects.filter(
        deadline__gte=today  # 마감일이 오늘 날짜 이후인 항목
    ).annotate(
        deadline_date=TruncDate('deadline')  # deadline을 날짜로 변환 (시간 부분 제거)
    ).annotate(
        days_remaining=F('deadline_date') - today  # 남은 시간 계산 (날짜 차이)
    ).order_by('days_remaining')[:3]

    # 클래스룸에서 남은 일수 추출
    for assignment in classroom:
    # timedelta에서 .days만 추출하여 저장
        assignment.days_remaining = assignment.days_remaining.days
        
    # 캘린더 
    today = date.today()  # 날짜 계산을 위해 'today' 다시 정의
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    cal = calendar.Calendar()
    month_days = cal.itermonthdays4(year, month)

    # 달력 구조 만들기
    calendar_data = []
    week = []
    for day in month_days:
        if day[1] != month:  # 현재 달이 아닌 날짜는 비어있는 셀로 처리
            week.append(None)
        else:
            week.append(day[2])  # 현재 날짜를 추가
        if len(week) == 7:  # 한 주가 끝나면 추가
            calendar_data.append(week)
            week = []
    if week:  # 마지막 남은 주 추가
        calendar_data.append(week)

    context = {
        'documents': documents,
        'calendar_data': calendar_data,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'classroom': classroom,
        'today': today
    }

    return HttpResponse(template.render(context, request))

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
    if search:
        #title_icontains: 대소문자 구분없이 문자열이 존재하는지 확인
        documents = Documents.objects.filter(title__icontains=search)
        count = len(documents)
    else:
        documents = Documents.objects.all()
        count = len(documents)

    context = {
        'documents':documents,
        'count': count
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
    if search:
        #title_icontains: 대소문자 구분없이 문자열이 존재하는지 확인
        assignments = Assignments.objects.filter(title__icontains=search)
        count = len(assignments)
    else:
        assignments = Assignments.objects.all()
        count = len(assignments)

    context = {
        'assignments':assignments,
        'count': count
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
    assignment_id = request.POST['assignment_id']
    author = request.session['login_user_name']
    email = request.session['login_ok_user']
    uploaded_file = request.FILES.get('attached')
    
    comments = Comments(assignment_id=assignment_id, author=author, email=email, attached=uploaded_file)
    comments.save()

    return HttpResponseRedirect(reverse('classroom_content',args=[assignment_id]))

def classroom_comment_delete(request, id):
    comment = Comments.objects.get(id=id)
    assignment_id = comment.assignment.id 
    comment.delete()
    
    return HttpResponseRedirect(reverse('classroom_content',args=[assignment_id]))

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

def att_write_ok(request):
    writer = request.session['login_user_name']
    title = '출결 관리 요청'
    content = request.POST['content']
    request_type = request.POST['request_type']
    request_date = request.POST['request_date']
    files = request.FILES.get('files')
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

    attendancerequest = AttendanceRequest(writer=writer, title=title, content=content, rdate = nowDatetime,
                                        request_date=request_date, request_type=request_type, files=files)
    attendancerequest.save()

    return HttpResponseRedirect(reverse('attendance'))

def att_request_update(request, id):
    template = loader.get_template('attendance/att_request_update.html')
    
    requests = AttendanceRequest.objects.get(id=id)
    context = {
        'requests':requests,
        "request_type_options": ["휴가", "결석", "지각", "병가", "조퇴", "예비군", "입사 시험", "입사 면접", "자격증", "사망", "외출", "실업 급여 관련 출석", "기타"],
    }

    return HttpResponse(template.render(context, request))


def att_request_update_ok(request, id):
    
    content = request.POST['content']
    request_type = request.POST['request_type']
    request_date = request.POST['request_date']
    files = request.FILES.get('files')
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    
    requests = AttendanceRequest.objects.get(id=id)
    requests.content = content
    requests.request_date = request_date
    requests.request_type = request_type
    requests.files = files
    requests.rdate = nowDatetime
    
    requests.save()
    
    return HttpResponseRedirect(reverse('att_request_details',args=[id]))


def att_request_delete(request,id):
    
    requests = AttendanceRequest.objects.get(id=id)
    requests.delete()
    
    return HttpResponseRedirect(reverse('attendance'))