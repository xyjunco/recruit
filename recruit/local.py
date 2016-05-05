# coding=utf-8
__author__ = 'junco'
__date__ = ''
# 所有与request请求无关，不返回Response的本地方法均实现于此

from django.core.exceptions import MultipleObjectsReturned
import json
import logging

from models import *


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='recruit.log')


def handle_resume2tags(tags):
    '''
    本地方法，处理上传的简历所包含的标签
    :param tags: 简历上传时所附加的标签信息，list对象
    :return: JSON序列化后的标签对象
    '''
    result = []
    for tag in tags:
        try:
            obj, created = Tag.objects.get_or_create(tag_name=tag)
            result.append(obj.id)
        except MultipleObjectsReturned:
            logging.error(u'标签库中存在重复标签：{0}'.format(tag))
        except Exception, e:
            logging.error(u'处理简历标签时出错：{0}'.format(e))

    return result


def handle_tag2resume(resume_id, tags):
    '''
    处理标签和简历之间的对应关系
    :param resume_id: 该简历ID
    :return: 无
    '''
    for tag in tags:
        try:
            obj = Tag.objects.filter(id=tag)[0]
            # 如果当前标签下属简历列表为空，则直接将该简历加入记录
            if not obj.tag_to_resume:
                obj.tag_to_resume = json.dumps([resume_id])
            # 如果不为空，则将该简历添加进去
            else:
                list = json.loads(obj.tag_to_resume)
                list.append(resume_id)
                obj.tag_to_resume = json.dumps(list)
            obj.save()
        except Exception, e:
            logging.error(u'处理标签对应的简历ID为{0}时出错：{1}'.format(resume_id, e))


def remove_resume_id_from_tag(resume):
    '''
    从标签表中移除标签到该简历的映射关系
    :param obj: 即将要被删除的简历对象
    :return: 无
    '''
    # 先找出该简历都对应哪些标签
    tags = json.loads(resume.resume_tags)
    for tag in tags:
        try:
            # 找到标签对象
            obj = Tag.objects.filter(id=tag)[0]
            list = json.loads(obj.tag_to_resume)
            # 从该标签对象的映射关系字段中，将到该简历的映射关系删除
            list.remove(resume.id)
            obj.tag_to_resume = json.dumps(list)
            obj.save()
        except Exception, e:
            logging.error(u'在解除标签{0}到简历{1}的映射关系时发生错误：{2}'.format(tag, resume.resume_name, e))

