# coding=utf-8

__author__ = 'junco'
__date__ = ''

from django.http import HttpResponse
from datetime import datetime
import logging
import json
import os

from models import *
from local import handle_resume2tags, handle_tag2resume, remove_resume_id_from_tag

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='recruit.log')

test_id = 123
test_people = 'Junco'


def get_recruit_msg(request):
    '''
    异步获取  从RecruitMsg表中读出最新的招聘动态信息
    :param request: request请求对象
    :return: JSON格式化后的动态信息
    '''
    result = []
    # 从数据库中读取出招聘动态信息
    # TODO：目前是取出所有的动态，考虑到以后如果招聘信息过多的话，只取出最新的前100条？
    msgs = RecruitMsg.objects.all()
    for msg in msgs:
        # 如果数据库中的截至日期为空的话，就将截至信息不予显示
        endtime = msg.recruit_endtime.strftime("%Y-%m-%d %H:%M") if msg.recruit_endtime is not None else ''
        record = {
            'id': msg.id,
            'person_name': msg.person_name,
            'recruit_title': msg.recruit_title,
            'recruit_posttime': msg.recruit_posttime.strftime("%Y-%m-%d %H:%M"),
            'recruit_endtime': endtime
        }
        result.append(record)
    # DataTables Ajax请求数据时要求返回{'data': []}的形式，因此在此进行包装处理
    return HttpResponse(json.dumps({'data': result}))


def commit_recruit_news(request):
    '''
    前端通过POST请求将新招聘动态提交到后台
    :param request: request
    :return: 提交、数据库写入结果，返回json串
    '''
    title = request.POST[u'title']
    company = request.POST[u'company']
    endtime = request.POST[u'endtime']
    detail = request.POST[u'detail']

    time = datetime.now()

    # TODO: 考虑一下当endtime为空的情况，向datetime字段存入空字符串会引起错误
    try:
        RecruitMsg.objects.create(
            person_id=test_id,
            person_name=test_people,
            recruit_title=title,
            recruit_company=company,
            recruit_posttime=time,
            recruit_endtime=endtime,
            recruit_content=detail
        )
        create_news(test_id,
                    test_people,
                    u'%s发布了一条新招聘动态：%s' % (test_people, title),
                    time,
                    '#')

    except Exception, e:
        logging.error(u'%s向数据库写入新招聘信息失败: %s' % (test_people, e))
        return HttpResponse(json.dumps({'result': False, 'message': e}))

    logging.info(u'%s向数据表Recruit_Msg中写入了一条招聘信息：%s' % (test_people, title))
    return HttpResponse(json.dumps({'result': True, 'message': 'success'}))



def get_communications_msg(request):
    '''
    异步获取  从Interview表中读出最新的面试经历分享信息
    :param request: request对象
    :return: JSON格式化后的面试经历分享信息
    '''
    result = []
    # 从数据库中读取出面试经历分享信息
    # TODO：目前是取出所有的动态，考虑到以后如果信息过多的话，只取出最新的前100条？
    msgs = Interview.objects.all()
    for msg in msgs:
        record = {
            'id': msg.id,
            'person_name': msg.person_name,
            'interview_title': msg.interview_title,
            'interview_company': msg.interview_company,
            'interview_time': msg.interview_time.strftime("%Y-%m-%d %H:%M")
        }
        result.append(record)
    # DataTables Ajax请求数据时要求返回{'data': []}的形式，因此在此进行包装处理
    return HttpResponse(json.dumps({'data': result}))


def commit_communication(request):
    '''
    前端向后台提交面试经验分享贴子
    :param request: request
    :return: 提交、数据库写入结果
    '''
    title = request.POST[u'title']
    company = request.POST[u'company']
    interview_time = request.POST[u'interview_time']
    interview_way = request.POST[u'interview_way']
    interview_class = request.POST[u'interview_class']
    detail = request.POST[u'detail']

    time = datetime.now()

    try:
        Interview.objects.create(
            person_id=test_id,
            person_name=test_people,
            interview_title=title,
            interview_company=company,
            interview_time=interview_time,
            interview_way=interview_way,
            interview_class=interview_class,
            interview_content=detail
        )
        create_news(test_id, test_people,
                    u'%s发布了一条新面试经历分享：%s' % (test_people, title),
                    time, '#')

    except Exception, e:
        logging.error(u'%s创建新面试经历时，向表Interview写入数据失败: %s' % (test_people, e))
        return HttpResponse(json.dumps({'result': False, 'message': e}))

    logging.info(u'%s创建了一条新面试经历，向表Interview中写入了一条新数据' % test_people)
    return HttpResponse(json.dumps({'result': True, 'message': 'success'}))



def get_calendar_events(request):
    '''
    从Calendar表中读取出所有招聘事件
    :param request: request对象
    :return: JSON格式化后的事件数组
    '''
    result = []
    start = str(request.GET['start'])
    end = str(request.GET['end'])

    try:
        events = Calendar.objects.filter(is_avaliable=True, event_starttime__range=(start, end))
        for event in events:
            result.append({
                'id': event.id,
                'title': event.event_title,
                'start': event.event_starttime.strftime('%Y-%m-%d %H:%M:%S'),
                'end': event.event_endtime.strftime('%Y-%m-%d %H:%M:%S'),
                'allDay': event.event_allday,
                'color': event.event_bgcolor
            })
    except Exception, e:
        logging.error('获取招聘日历信息时出错: %s' % e)
        return HttpResponse('false')

    return HttpResponse(json.dumps(result))


def commit_calendar_event(request):
    '''
    向“招聘日历”中添加新事件，通过POST请求提交，由该方法进行处理
    :param request: request对象
    :return: 提交结果
    '''
    event = request.POST['event']
    start = request.POST['start']
    end = request.POST['end']
    color = request.POST['color']

    try:
        Calendar.objects.create(
            person_id=test_id,
            person_name=test_people,
            event_title=event,
            event_starttime=start,
            event_endtime=end,
            # 当前版本中设计增加的事件全部为全天事件，所以该字段一直为true,后续版本中考虑增加具体时间，故该字段保留
            event_allday=True,
            event_bgcolor=color,
            is_avaliable=True
        )
    except Exception, e:
        logging.error(u'%s向日历中新建事件时发生错误：%s' % (test_people, e))
        return HttpResponse(json.dumps({'result': False, 'message': e}))

    logging.info(u'%s向日历中新添加了一条事件：%s' % (test_people, event))
    return HttpResponse(json.dumps({'result': True, 'message': 'success'}))


def update_calendar_event(request):
    '''
    “招聘日历”中事件更新
    :param request: request对象
    :return: 更新结果
    '''
    id = int(request.POST['id'])
    event = request.POST['event']
    start = request.POST['start']
    end = request.POST['end']
    color = request.POST['color']

    try:
        Calendar.objects.filter(id=id, is_avaliable=True).update(
            event_title=event,
            event_starttime=start,
            event_endtime=end,
            event_bgcolor=color
        )
    except Exception, e:
        logging.error(u'%s更新日历中ID为%s的事件，但是在更新信息时出错：%s' % (test_people, id, e))
        return HttpResponse(json.dumps({'result': False, 'message': e}))

    logging.info(u'%s更新了日历中ID为%s的事件' % (test_people, id))
    return HttpResponse(json.dumps({'result': True, 'message': 'success'}))


def delete_calendar_event(request):
    '''
    删除“招聘日历”中的事件
    :param request:
    :return:
    '''
    id = request.POST['id']

    try:
        Calendar.objects.filter(id=id, is_avaliable=True).update(is_avaliable=False)
    except Exception, e:
        logging.error(u'%s在招聘日历中删除ID为%s的信息时失败:%s' % (test_people, id, e))
        return HttpResponse(json.dumps({'result': False, 'message': e}))

    logging.info(u'%s删除了招聘日历中ID为%s的信息' % (test_people, id))
    return HttpResponse(json.dumps({'result': True, 'message': 'success'}))


def upload_resume(request):
    '''
    用户上传新简历
    :param request: request对象
    :return: 上传结果
    '''
    resume = request.FILES.get('file', '')
    resume_desc = request.POST['resume_desc']
    tags = json.loads(request.POST['tags'])

    if resume:
        # 文件合法性二次判断
        if resume.content_type != u'application/pdf':
            return HttpResponse(json.dumps({'result': False, 'message': '仅支持PDF格式文件！'}))
        if resume.size > 1024 * 1024:
            return HttpResponse(json.dumps({'result': False, 'message': '最大仅支持上传1M的文件！'}))

        try:
            obj = ResumeMsg(
                person_id=test_id,
                person_name=test_people,
                resume_name=resume.name,
                resume_desc=resume_desc,
                resume_path=resume,
                upload_time=datetime.now(),
                is_gathered=False
            )
            obj.save()
        except Exception, e:
            logging.error(u'%s上传了一份简历：%s，存储时发生错误%s' % (test_people, resume.name, e))
            return HttpResponse(json.dumps({'result': False, 'message': e}))

        # 上传成功并存储成功后，调用pdf2img模块来生成该简历的缩略图，用于前端展示
        os.system('pdf2img %s' % obj.resume_path.path)
        obj.resume_thumb = '/static/thumbs/' + os.path.basename(obj.resume_path.path).split('.')[0] + '.png'
        # 处理简历和标签之间的对应关系
        tag_list = handle_resume2tags(tags)
        handle_tag2resume(obj.id, tag_list)

        obj.resume_tags = json.dumps(tag_list)
        obj.save()

    else:
        logging.error(u'%s上传了一份简历，但由于传输过程中发生了错误，服务器端读取简历失败' % test_people)
        return HttpResponse(json.dumps({'result': False, 'message': '由于传输过程中发生了错误，服务器端读取简历失败'}))

    create_news(id=test_id, name=test_people,
                title=u'%s上传了一份新简历' % test_people,
                time=datetime.now(), url='#')

    logging.info(u'%s上传了一份简历：%s' % (test_people, resume.name))
    return HttpResponse(json.dumps({'result': True, 'message': {
        'resume_id': obj.id,
        'resume_name': obj.resume_name,
        'resume_desc': obj.resume_desc,
        'upload_time': obj.upload_time.strftime("%Y-%m-%d %H:%M"),
        'resume_thumb': obj.resume_thumb,
        'resume_url': obj.resume_path.url,
        'is_gathered': obj.is_gathered
    }}))


def change_resume_gathered(request):
    '''
    更改简历状态，可发生事件有两种：【1】可被收集 -> 不可被收集  【2】不可被收集 -> 可被收集
    :param request: request对象
    :return: 更改结果，JSON格式
    '''
    resume_id = int(request.POST['id'])

    try:
        obj = ResumeMsg.objects.filter(id=resume_id)[0]
        obj.is_gathered = not obj.is_gathered
        obj.save()
    except Exception, e:
        logging.error(u'{0}在更改简历ID={1}时发生错误：{2}'.format(test_people, obj.id, e))
        return HttpResponse(json.dumps({'result': False, 'message': e}))

    logging.info(u'{0}更改了简历ID＝{1}的状态'.format(test_people, obj.id))
    return HttpResponse(json.dumps({'result': True, 'message': 'success'}))


def delete_resume(request):
    '''
    删除简历 简历ID由request中参数来指出
    :param reqeuest: Request对象
    :return: 删除结果
    '''
    id = request.POST['id']

    try:
        obj = ResumeMsg.objects.filter(id=id)[0]
        remove_resume_id_from_tag(obj)
        obj.delete()
    except Exception, e:
        logging.error(u'{0}在删除简历ID={1}时发生了错误：{2}'.format(test_people, id, e))
        return HttpResponse(json.dumps({'result': False, 'message': e}))

    logging.info(u'{0}删除了简历ID＝{1}'.format(test_people, id))
    return HttpResponse(json.dumps({'result': True, 'message': 'success'}))


def get_tags(request):
    '''
    标签接口：从数据库中取出所有可用标签名称
    :param request: request对象
    :return: 标签名list
    '''
    # 从Tag表中取出每一个tag_name值，注意values_list返回结果仍为QuerySet
    tags = Tag.objects.values_list('tag_name', flat=True)
    # 对每一个tag_name对象作用于str方法，序列化后返回
    return HttpResponse(json.dumps(map(str, tags)))


def create_news(id, name, title, time, url):
    '''
    向News表中新增一条新动态
    :param id: 新动态创建者ID
    :param name: 新动态创建者姓名
    :param title: 新动态标题
    :param time: 新动态产生时间
    :param url: 对应页面url
    :return: 无
    '''
    try:
        News.objects.create(
            person_id=id,
            person_name=name,
            news_title=title,
            news_time=time,
            news_url=url
        )
    except Exception, e:
        logging.error(u'向数据库动态表中生成新动态失败: %s' % e)
