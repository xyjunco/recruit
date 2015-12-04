# coding=utf-8
__author__ = 'junco'
__date__ = ''


from django.contrib import admin
from .models import *


class ResumeCommentAdmin(admin.TabularInline):
    model = ResumeComment
    fields = ['resume', 'person_id', 'person_name', 'comment_time', 'comment_content']
    list_display = ['resume', 'person_name', 'comment_time', 'comment_content']


class ResumeMsgAdmin(admin.ModelAdmin):
    inlines = [ResumeCommentAdmin]
    fields = ['person_id', 'person_name', 'resume_name', 'resume_path', 'upload_time', 'is_gathered', 'resume_tags']
    list_display = ['person_name', 'resume_name', 'resume_path', 'upload_time', 'is_gathered']
    search_fields = ['person_name', 'resume_name', 'upload_time']
    list_filter = ['upload_time']


class RecruitCommentAdmin(admin.TabularInline):
    model = RecruitComment
    fields = ['resume', 'person_id', 'person_name', 'comment_time', 'comment_content']
    list_display = ['resume', 'person_name', 'comment_time', 'comment_content']


class RecruitMsgAdmin(admin.ModelAdmin):
    inlines = [RecruitCommentAdmin]
    fields = ['person_id', 'person_name', 'recruit_title', 'recruit_company', 'recruit_posttime', 'recruit_endtime', 'recruit_content']
    list_display = ['person_name', 'recruit_title', 'recruit_company', 'recruit_posttime', 'recruit_endtime', 'recruit_content']
    search_fields = ['person_name', 'recruit_title', 'recruit_company', 'recruit_posttime']
    list_filter = ['recruit_posttime']


class InterviewAdmin(admin.ModelAdmin):
    fields = ['person_id', 'person_name', 'interview_title', 'interview_company', 'interview_time', 'interview_way', 'interview_class']
    list_display = ['person_name', 'interview_title', 'interview_company', 'interview_time', 'interview_way', 'interview_class']
    search_fields = ['person_name', 'interview_title', 'interview_company']
    list_filter = ['interview_time']


class NewsAdmin(admin.ModelAdmin):
    fields = ['person_id', 'person_name', 'news_title', 'news_time', 'news_url']
    list_display = ['person_id', 'person_name', 'news_title', 'news_time', 'news_url']
    search_fields = ['person_name', 'news_title']
    list_filter = ['news_time']


class CalendarAdmin(admin.ModelAdmin):
    fields = ['person_id', 'person_name', 'event_title', 'event_starttime', 'event_endtime', 'event_allday', 'event_bgcolor']
    list_display = ['person_id', 'person_name', 'event_title', 'event_starttime', 'event_endtime', 'event_bgcolor', 'is_avaliable']
    search_fields = ['person_name', 'event_title']
    list_filter = ['event_starttime']


class TagAdmin(admin.ModelAdmin):
    fields = ['tag_name', 'tag_to_resume']
    list_display = ['tag_name', 'tag_to_resume']
    search_fields = ['tag_name']


admin.site.register(ResumeMsg, ResumeMsgAdmin)
admin.site.register(RecruitMsg, RecruitMsgAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Tag, TagAdmin)