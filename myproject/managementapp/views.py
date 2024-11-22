from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Documents, Member
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
    template = loader.get_template('notices.html')
    documents = Documents.objects.all()
    context = {
        'documents':documents
    }
    return HttpResponse(template.render(context,request))

def notice_content(request,id):
    template = loader.get_template('notice_content.html')
    document=Documents.objects.get(id=id)
    context = {
        'document': document
    }
    return HttpResponse(template.render(context,request))
    
def notice_update(request,id):
    template = loader.get_template('notice_update.html')
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
    template = loader.get_template('notice_delete.html')
    print('template 호출 완료')
    document = Documents.objects.get(id=id)
    context = {
        'document': document
    }
    print(f"전달할 context: {context}")

    return HttpResponse(template.render(context,request))

def notice_delete_ok(request,id):
    
    document = Documents.objects.get(id=id)
    document.delete()
    return HttpResponseRedirect(reverse('notices'))

#classroom
def classroom(request):
    template = loader.get_template('classroom.html')
    
    return HttpResponse(template.render({},request))


#attendance
def attendance(request):
    template = loader.get_template('attendance.html')
    
    return HttpResponse(template.render({},request))