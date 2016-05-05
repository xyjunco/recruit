# coding=utf-8

"""recruit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from recruit import views, ajax, comments


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', views.home, name='home'),
    url(r'^calendar/', views.calendar, name='calendar'),
    url(r'^communicate/', views.communicate, name='communicate'),
    url(r'^my_resume/', views.my_resume, name='my_resume'),

    # 招聘动态相关接口
    url(r'^get_recruit_msg/', ajax.get_recruit_msg, name='get_recruit_msg'),
    url(r'^commit_recruit_news/', ajax.commit_recruit_news, name='commit_recruit_news'),
    url(r'^recruit/(.+)/$', views.recruit, name='news'),
    url(r'^api/recruit/comments/(.+)/$', comments.get_comments, name='get_comments'),

    # 招聘日历接口
    url(r'^get_calendar_events/', ajax.get_calendar_events, name='get_calendar_events'),
    url(r'^commit_calendar_event/', ajax.commit_calendar_event, name='commit_calendar_event'),
    url(r'^update_calendar_event/', ajax.update_calendar_event, name='update_calendar_event'),
    url(r'^delete_calendar_event/', ajax.delete_calendar_event, name='delete_calendar_event'),

    # 面试经历交流接口
    url(r'^get_communications_msg/', ajax.get_communications_msg, name='commit_communication'),
    url(r'^commit_communication/', ajax.commit_communication, name='commit_communication'),
    url(r'communication/(.+)/$', views.communication, name='communication_detail'),

    # 我的简历接口
    url(r'^resume/(.+)/$', views.resume, name='resume'),
    url(r'^upload_resume/', ajax.upload_resume, name='upload_resume'),
    url(r'^change_resume_gathered/', ajax.change_resume_gathered, name='change_resume_gathered'),
    url(r'^delete_resume/', ajax.delete_resume, name='delete_resume'),
    url(r'^api/resume/comments/(.+)/$', comments.get_comments, name='get_comments'),
    url(r'^api/resume/post_comment/(.+)/$', comments.post_comment, name='post_comments'),
    url(r'^api/resume/update_comment/(.+)/$', comments.update_comment, name='update_comment'),
    url(r'^api/resume/delete_comment/(.+)/$', comments.delete_comment, name='delete_comment'),
    url(r'^api/resume/upvote/(.+)/$', comments.upvote, name='upvote'),



    # 成员简历接口
    url(r'^resume_by_group/', views.resume_by_group, name='resume_by_group'),

    # 简历过滤接口
    url(r'^screen/', views.screen, name='screen'),

    # 标签相关接口
    url(r'^get_tags/', ajax.get_tags, name='get_tags')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
