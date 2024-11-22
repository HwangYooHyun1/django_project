from django.urls import path
from . import views

urlpatterns = [
    #login
    path('', views.login, name='login'),
    path('login_ok/', views.login_ok, name='login_ok'),
    path('logout/', views.logout, name='logout'),
    #home
    path('home/',views.home, name='home'),
    #notices
    path('notices/',views.notices, name='notices'),
    path('notices/content/<int:id>',views.notice_content, name='notice_content'),
    path('notices/update/<int:id>',views.notice_update, name='notice_update'),
    path('notices/notice_update_ok/<int:id>',views.notice_update_ok, name='notice_update_ok'),
    path('notices/delete/<int:id>',views.notice_delete, name='notice_delete'),
    
    #classroom
    path('classroom/',views.classroom, name='classroom'),
    
    #attendance
    path('attendance/',views.attendance, name='attendance'),
    
    
    
]

