from django.urls import path
from . import views

urlpatterns = [
    #login
    path('', views.login, name='login'),
    path('login_ok/', views.login_ok, name='login_ok'),
    path('logout/', views.logout, name='logout'),
    path('join/', views.join, name='join'),
    path('join_ok/', views.join_ok, name='join_ok'),
    
    #home
    path('home/',views.home, name='home'),

    #myinfo
    path('myinfo/',views.myinfo, name='myinfo'),
    path('myinfo/update', views.myinfo_update, name='myinfo_update'),
    path('myinfo/update_ok', views.myinfo_update_ok, name='myinfo_update_ok'),
    #notices
    path('notices/',views.notices, name='notices'),
    path('notices/write/',views.notice_write, name='notice_write'),
    path('notices/write_ok',views.notice_write_ok, name='notice_write_ok'),
    path('notice_search/',views.notice_search, name='notice_search'),
    path('notices/content/<int:id>',views.notice_content, name='notice_content'),
    path('notices/update/<int:id>',views.notice_update, name='notice_update'),
    path('notices/notice_update_ok/<int:id>',views.notice_update_ok, name='notice_update_ok'),
    path('notices/delete/<int:id>',views.notice_delete, name='notice_delete'),

    #classroom
    path('classroom/',views.classroom, name='classroom'),
    path('classroom/write/',views.classroom_write, name='notice_write'),
    path('classroom/write_ok',views.classroom_write_ok, name='classroom_write_ok'),
    path('classroom_search/',views.classroom_search, name='classroom_search'),
    path('classroom/content/<int:id>',views.classroom_content, name='classroom_content'),
    path('classroom/content/comment_insert',views.classroom_comment, name='classroom_comment'),
    path('classroom/content/comment_delete/<int:id>',views.classroom_comment_delete, name='classroom_comment_delete'),
    path('classroom/update/<int:id>',views.classroom_update, name='classroom_update'),
    path('classroom/classroom_update_ok/<int:id>',views.classroom_update_ok, name='classroom_update_ok'),
    path('classroom/delete/<int:id>',views.classroom_delete, name='classroom_delete'),

    #attendance
    path('attendance/',views.attendance, name='attendance'),
    path('attendance/notice_content/<int:id>',views.att_notice_content, name='att_notice_content'),
    path('attendance/requestdetails/<int:id>',views.att_request_details, name='att_request_details'),
    path('attendance/write/',views.att_write, name='att_write'),
    path('attendance/write_ok',views.att_write_ok, name='att_write_ok'),
    path('attendance/notice/update/<int:id>',views.att_notice_update, name='att_notice_update'),
    path('attendance/notice/notice_update_ok/<int:id>',views.att_notice_update_ok, name='att_notice_update_ok'),
    path('attendance/request/update/<int:id>',views.att_request_update, name='att_request_update'),
    path('attendance/request/request_update_ok/<int:id>',views.att_request_update_ok, name='att_request_update_ok'),
    path('attendance/request/delete/<int:id>',views.att_request_delete, name='att_request_delete'),
]

