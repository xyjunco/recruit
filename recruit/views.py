# coding=utf-8
__author__ = 'junco'
__date__ = ''

from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

from models import *


# 最新动态所展示的新闻条数，默认为5条，可在此设置
news_count = 5


def home(request):
    '''
    主页
    :param request: request对象
    :return: news.html (渲染进base.html里)
    '''
    return render_to_response('news.html', {'newslist': get_newslist()})


def calendar(request):
    '''
    校招日历
    :param request: request对象
    :return: calendar.html (渲染进base.html里)
    '''
    return render_to_response('calendar.html', {'newslist': get_newslist()})


def communication(requtest):
    '''
    面试交流 版块
    :param requtest: request对象
    :return: communication.html （渲染进base.html里）
    '''
    return render_to_response('communication.html', {'newslist': get_newslist()})


def my_resume(request):
    '''
    我的简历  版块
    :param request:
    :return:
    '''
    data = []
    objs = ResumeMsg.objects.filter(person_name='Junco')

    # 如果当前用户已上传过简历
    if len(objs) != 0:
        for obj in objs:
            data.append({
                'id': obj.id,
                'resume_name': obj.resume_name,
                'resume_desc': obj.resume_desc,
                'upload_time': obj.upload_time,
                'resume_path': obj.resume_path,
                'resume_thumb': obj.resume_thumb,
                'is_gathered': obj.is_gathered
            })

    return render_to_response('my_resume.html', {
        'newslist': get_newslist(),
        'resumes': data
    })


def resume(request):
    '''

    :param request:
    :return:
    '''
    resume_id = request.GET.get('id')
    obj = ResumeMsg.objects.filter(id=resume_id)[0]

    return render_to_response('resume.html', {'resume_url': obj.resume_path.url})


def get_newslist():
    '''
    从数据库News表中取出最新的news_count条新闻
    :return: newslist
    '''
    newslist = []
    try:
        objs = News.objects.order_by('-news_time')[0:news_count]
        for obj in objs:
            newslist.append({
                'news_url': obj.news_url,
                'news_title': obj.news_title,
                'news_time': obj.news_time,
            })
    except:
        newslist = []

    return newslist
