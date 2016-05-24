# coding=utf-8
__author__ = 'junco'
__date__ = ''

# 评论相关，评论系统采用JQuery-Comments插件，获取评论、新增评论等操作在此模块中完成

import json
import logging
from django.http import JsonResponse
from django.db.models import F

from models import *


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='recruit.log')


test_id = 1009
test_people = 'Junco'


def get_object(request, obj_id):
    '''
    判断请求来源是简历页面还是动态评论页面，并返回简历/动态实体
    :param request: request请求
    :param obj_id: 简历/动态ID
    :return: 简历/动态Object
    '''
    try:
        if 'recruit' in request.path:
            obj = RecruitMsg.objects.get(id=obj_id)
        if 'resume' in request.path:
            obj = ResumeMsg.objects.get(id=obj_id)
    except Exception, e:
        logging.error(u'获取评论内容失败：%s' % e)
        return None

    return obj


def get_comments(request, obj_id):
    '''
    获取所有评论信息
    :param request: request请求
    :param obj_id: 当前简历/动态object的ID
    :return: 该简历/动态所对应的所有评论
    '''
    resultlist = []

    # 找出当前动态/简历对应的object
    obj = get_object(request, obj_id)
    if obj is None:
        return JsonResponse({'result': False, 'message': '获取评论信息失败！'})

    # 判断是要从简历中还是要从招聘动态中取出评论
    if isinstance(obj, RecruitMsg):
        comments = RecruitComment.objects.filter(recruit=obj)
    if isinstance(obj, ResumeMsg):
        comments = ResumeComment.objects.filter(resume=obj)

    # 如果没有评论  则返回空
    if comments.count() == 0:
        return JsonResponse('')

    for comment in comments:
        if comment.comment_modified:
            modified = comment.comment_modified.strftime("%Y-%m-%d %H:%M")
        else:
            modified = ''

        # 获取所有点赞人ID列表
        upvoted_list = json.loads(comment.userHasUpvoted)
        if test_id in upvoted_list:
            comment.userHasUpvoted = True
        else:
            comment.userHasUpvoted = False
        result = {
            'id': comment.id,
            'parent': comment.comment_parent,
            'created': comment.comment_created.strftime("%Y-%m-%d %H:%M"),
            'modified': modified,
            'content': comment.comment_content,
            'fullname': comment.person_name,
            'profile_picture_url': comment.profilePictureURL,
            'created_by_current_user': True,
            'upvote_count': comment.upvoteCount,
            'user_has_upvoted': comment.userHasUpvoted
        }
        resultlist.append(result)

    return JsonResponse(resultlist, safe=False)


def post_comment(request, objid):
    '''
    新增加一条新评论
    :param request: request对象
    :param objid: 前端传来的新评论所对应的简历编号
    :return: 后台操作结果
    '''
    # 简历/招聘信息对象ID值 ，根据此ID值获得对象实体
    obj = get_object(request, int(str(objid)))

    # 该条评论父节点，如果没有父节点则设置为0
    parent = request.POST[u'data[parent]'] or 0
    # 这个时间有点恶心，要把TZ时间处理成普通时间
    created = request.POST[u'data[created]'].split('.')[0].replace('T', ' ')

    # 如果评论的是简历
    if isinstance(obj, ResumeMsg):
        try:
            ResumeComment.objects.create(
                resume=obj,
                person_id=test_id,
                person_name=test_people,
                comment_parent=int(parent),
                comment_created=created,
                comment_content=request.POST[u'data[content]'],
            )
        except Exception, e:
            logging.error(u'评论简历ID＝{0}时发生错误：{1}'.format(obj.id, e))
            return JsonResponse({'result': False, 'message': e})

    # 如果评论的是招聘动态
    if isinstance(obj, RecruitMsg):
        try:
            RecruitComment.objects.create(
                recruit=obj,
                person_id=test_id,
                person_name=test_people,
                comment_parent=int(parent),
                comment_created=created,
                comment_content=request.POST[u'data[content]'],
            )
        except Exception, e:
            logging.error(u'评论招聘信息ID＝{0}时发生错误：{1}'.format(obj.id, e))
            return JsonResponse({'result': False, 'message': e})

    return JsonResponse({'result': True, 'message': 'success'})


def update_comment(request, objid):
    '''
    更新一条已有评论
    :param request: Reuqest对象
    :param objid: 前端传来的需要修改的评论对应的简历/招聘信息ID
    :return: 修改结果
    '''
    obj = get_object(request, int(str(objid)))

    comment_id = request.POST[u'data[id]']
    new_comment = request.POST[u'data[content]']

    # 如果修改的是简历的评论
    if isinstance(obj, ResumeMsg):
        try:
            ResumeComment.objects.filter(resume=obj, id=comment_id).update(comment_content=new_comment)
        except Exception, e:
            logging.error(u'更新简历ID＝{0}的评论ID＝{1}时发生错误：{2}'.format(obj.id, comment_id, e))
            return JsonResponse({'result': False, 'message': e})

    # 如果评论的是招聘动态的评论
    if isinstance(obj, RecruitMsg):
        try:
            RecruitComment.objects.filter(recruit=obj, id=comment_id).update(comment_content=new_comment)
        except Exception, e:
            logging.error(u'更新招聘信息ID＝{0}的评论ID={1}发生错误：{2}'.format(obj.id, comment_id, e))
            return JsonResponse({'result': False, 'message': e})

    return JsonResponse({'result': True, 'message': 'success'})


def delete_comment(request, objid):
    '''
    删除一条评论信息
    :param request: Request对象
    :param objid: 前端传来的需要修改的评论对应的简历/招聘信息ID
    :return: 删除结果
    '''

    obj = get_object(request, int(str(objid)))
    comment_id = request.POST[u'data[id]']

    # 如果删除的是简历的评论
    if isinstance(obj, ResumeMsg):
        try:
            ResumeComment.objects.filter(resume=obj, id=comment_id).delete()
        except Exception, e:
            logging.error(u'删除简历ID＝{0}的评论ID＝{1}时发生错误：{2}'.format(obj.id, comment_id, e))
            return JsonResponse({'result': False, 'message': e})

    # 如果评论的是招聘动态的评论
    if isinstance(obj, RecruitMsg):
        try:
            RecruitComment.objects.filter(recruit=obj, id=comment_id).delete()
        except Exception, e:
            logging.error(u'删除招聘信息ID＝{0}的评论ID={1}发生错误：{2}'.format(obj.id, comment_id, e))
            return JsonResponse({'result': False, 'message': e})

    return JsonResponse({'result': True, 'message': 'success'})


def upvote(request, objid):
    '''
    用户点赞/取消赞
    :param request: Request对象
    :param objid: 前端传来的点赞的评论对应的简历/招聘信息ID
    :return: 处理结果
    '''

    obj = get_object(request, int(objid))
    comment_id = request.POST[u'data[id]']
    has_upvoted = request.POST[u'data[user_has_upvoted]']

    # 用户点赞
    if has_upvoted == u'true':
        power = 1
    # 用户取消点赞
    elif has_upvoted == u'false':
        power = -1

    # 如果点赞的是简历的评论
    if isinstance(obj, ResumeMsg):
        try:
            resume_obj = ResumeComment.objects.filter(resume=obj, id=comment_id)[0]
            resume_obj.upvoteCount += power
            list = json.loads(resume_obj.userHasUpvoted)
            if power > 0:
                list.append(test_id)
            else:
                list.remove(test_id)
            resume_obj.userHasUpvoted = json.dumps(list)

            resume_obj.save()
        except Exception, e:
            logging.error(u'点赞简历ID＝{0}的评论ID＝{1}时发生错误：{2}'.format(obj.id, comment_id, e))
            return JsonResponse({'result': False, 'message': e})

    # 如果点赞的是招聘动态的评论
    if isinstance(obj, RecruitMsg):
        try:
            recruit_obj = RecruitComment.objects.filter(recruit=obj, id=comment_id)[0]
            recruit_obj.upvoteCount += power
            list = json.loads(recruit_obj.userHasUpvoted)
            if power > 0:
                list.append(test_id)
            else:
                list.remove(test_id)
            recruit_obj.userHasUpvoted = json.dumps(list)

            recruit_obj.save()
        except Exception, e:
            logging.error(u'点赞招聘信息ID＝{0}的评论ID={1}发生错误：{2}'.format(obj.id, comment_id, e))
            return JsonResponse({'result': False, 'message': e})

    return JsonResponse({'result': True, 'message': 'success'})
