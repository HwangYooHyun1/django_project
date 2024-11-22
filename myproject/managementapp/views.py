from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Documents
from django.urls import reverse
from django.utils import timezone 

def home(request):
    template = loader.get_template('home.html')
    
    return HttpResponse(template.render({},request))


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
    
    return HttpResponse(template.render({},request))

def notice_delete_ok(request,id):
    
    document = Documents.objects.get(id=id)
    document.delete()
    return HttpResponseRedirect(reverse('notices'))

def classroom(request):
    template = loader.get_template('classroom.html')
    
    return HttpResponse(template.render({},request))

def attendance(request):
    template = loader.get_template('attendance.html')
    
    return HttpResponse(template.render({},request))