# coding=utf-8
__author__ = 'junco'
__date__ = ''

from django.http import HttpResponse
from django.shortcuts import render_to_response
from markdown2 import markdown
import logging
import json

from models import *


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='recruit.log')

# 最新动态所展示的新闻条数，默认为5条，可在此设置
news_count = 5


def home(request):
    '''
    主页
    :param request: request对象
    :return: news.html (渲染进base.html里)
    '''
    return render_to_response('news.html', {'newslist': get_newslist(), 'user': request.user})


def calendar(request):
    '''
    校招日历
    :param request: request对象
    :return: calendar.html (渲染进base.html里)
    '''
    return render_to_response('calendar.html', {'newslist': get_newslist(), 'user': request.user})


def communicate(requtest):
    '''
    面试交流 版块
    :param requtest: request对象
    :return: communicate.html （渲染进base.html里）
    '''
    return render_to_response('communicate.html', {'newslist': get_newslist(), 'user': requtest.user})


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
        'user': request.user,
        'resumes': data
    })


def resume(request, resume_id):
    '''
    个人简历具体页面，页面负责展示简历ID所对应简历的具体信息，简历ID通过GET方式传递
    :param request: request对象
    :return: 渲染后的resume页面，其中包括简历展示和他人评论内容。该页面继承自base.html
    '''
    obj = ResumeMsg.objects.filter(id=resume_id)[0]

    return render_to_response('resume.html', {
        'newslist': get_newslist(),
        'user': request.user,
        # 这里如果返回obj.resume_path.url，会将中文字符进行url编码处理，再进行访问时解析会出错
        # obj.resume_path.name会返回中文相对路径，手动加上'/media/'后补全为绝对路径返回前端
        'resume_url': '/media/' + obj.resume_path.name
    })


def recruit(request, news_id):
    '''
    招聘动态具体页面，展示所发布招聘动态的具体内容，以及相关回复、评论信息
    :param request: request对象
    :param news_id: 招聘动态ID
    :return:
    '''
    try:
        obj = RecruitMsg.objects.filter(id=news_id)[0]
    except Exception, e:
        logging.error(u'获取招聘动态详细信息(id=%s)失败: %s' % (news_id, e))
        return HttpResponse(u'获取招聘动态详细信息失败！id=%s' % news_id)

    return render_to_response('recruit_detail.html', {
        'newslist': get_newslist(),
        'user': request.user,
        'person_name': obj.person_name,
        'recruit_title': obj.recruit_title,
        'recruit_company': obj.recruit_company,
        'recruit_posttime': obj.recruit_posttime.strftime('%Y-%m-%d %H:%M:%S'),
        'recruit_endtime': obj.recruit_endtime.strftime('%Y-%m-%d %H:%M:%S'),
        'recruit_content': markdown(obj.recruit_content)
    })


def communication(request, interview_id):
    '''
    面经交流页面，展示所有用户所发表的面试经历具体信息以及其它用户的评论交流
    :param request: request对象
    :param com_id: 该条面经信息ID
    :return:
    '''
    try:
        obj = Interview.objects.filter(id=interview_id)[0]
    except Exception, e:
        logging.error(u'获取面试经历具体信息(id=%s)失败: %s' % (interview_id, e))
        return HttpResponse(u'获取招聘动态详细信息(id=%s)失败: %s' % (interview_id, e))

    return render_to_response('communication_detail.html', {
        'newslist': get_newslist(),
        'user': request.user,
        'person_name': obj.person_name,
        'interview_title': obj.interview_title,
        'interview_company': obj.interview_company,
        'interview_time': obj.interview_time.strftime('%Y-%m-%d'),
        'interview_way': obj.interview_way,
        'interview_class': obj.interview_class,
        'interview_content': obj.interview_content
    })



def resume_by_group(request):
    '''
    边栏中“成员简历”页面，负责按级展示成员简历
    :param request: request
    :return:
    '''

    return render_to_response('resume_by_group.html', {'newslist': get_newslist(), 'user': request.user})


def screen(request):
    '''
    边栏中“简历筛选”页面，用来针对指定的标签进行过滤
    :param request: request对象
    :return:
    '''

    return render_to_response('screen.html', {'newslist': get_newslist(), 'user': request.user})


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
