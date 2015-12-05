# coding=utf-8

__author__ = 'junco'
__date__ = '2015-10-18'

from django.db import models
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# 上传的简历，一个简历对应一个ResumeMsg对象
class ResumeMsg(models.Model):
    # 简历所属者姓名，默认不可为空
    person_id = models.IntegerField(verbose_name='发布人ID', null=False, blank=False)
    person_name = models.CharField(verbose_name='姓名', max_length=30, blank=False)
    # 简历文件名，可用于标注简历版本，针对哪一企业等信息
    resume_name = models.CharField(verbose_name='简历文件名', max_length=100, blank=True)
    # 简历描述，备注信息
    resume_desc = models.CharField(verbose_name='简历描述', max_length=100, blank=True)
    # 简历存放路径，默认上传到os.path.abspath(settings.py)目录下upload_to所指定的目录，可为空
    # upload_to字段全路径由settings.py中定义的 MEDIA_ROOT 所指定，即简历路径为 MEDIA_ROOT+upload_to
    resume_path = models.FileField(verbose_name='简历位置', upload_to='upload_files/', blank=True)
    # 缩略图路径
    resume_thumb = models.FilePathField(verbose_name='缩略图位置', path='upload_files/thumbs/', blank=True)
    # 上传日期时间，默认为时间戳
    upload_time = models.DateTimeField(verbose_name='上传时间', null=False, blank=False)
    # 当有学长收集简历时，该简历是否为可收集版本，如果设置为True，则会在收集时被自动打包
    is_gathered = models.BooleanField(verbose_name='可被收集', default=True)
    # 标签集合，该简历被打上的标签都会在此字段以JSON串记录，值为Tag表中标签的ID值
    resume_tags = models.TextField(verbose_name='标签值', null=True, blank=True)

    def __unicode__(self):
        return self.person_name + '的简历'


# 简历评论，一条评论对应一个Comment对象
class ResumeComment(models.Model):
    # 简历关连到ResumeMsg
    resume = models.ForeignKey(ResumeMsg)
    # 评论用户，默认不可为空
    person_id = models.IntegerField(verbose_name='发布人ID', null=False, blank=False)
    person_name = models.CharField(verbose_name='姓名', max_length=30, blank=False)
    # 评论时间
    comment_time = models.DateTimeField(verbose_name='评论时间', null=False, blank=False)
    # 评论内容
    comment_content = models.TextField(verbose_name='评论内容', blank=False)

    def __unicode__(self):
        return self.person_name + '的评论'


class Tag(models.Model):
    # 标签名
    tag_name = models.CharField(verbose_name='标签名', max_length=20, blank=False)
    # 所拥有该标签的简历，以JSON格式记录在该字段，值为对应简历（ResumeMsg）的ID值
    tag_to_resume = models.TextField(verbose_name='关联简历', blank=True)

    def __unicode__(self):
        return self.tag_name


# 招聘动态信息，一条新招聘信息对应一个RecruitMsg对象
class RecruitMsg(models.Model):
    # 动态发布者，默认不可为空
    person_id = models.IntegerField(verbose_name='发布人ID', null=False, blank=False)
    person_name = models.CharField(verbose_name='发布人', max_length=30, blank=False)
    # 招聘动态标题
    recruit_title = models.CharField(verbose_name='招聘动态标题', max_length=100, blank=False)
    # 招聘企业
    recruit_company = models.CharField(verbose_name='招聘企业', max_length=30, blank=False)
    # 动态发布日期
    recruit_posttime = models.DateTimeField(verbose_name='发布日期', null=False, blank=False)
    # 信息截至日期
    recruit_endtime = models.DateTimeField(verbose_name='截至日期', null=True, blank=True)
    # 动态内容
    recruit_content = models.TextField(verbose_name='招聘动态内容', blank=False)

    def __unicode__(self):
        return self.recruit_title + '(' + self.person_name + ')'


# 招聘动态评论，一条评论对应一个RecruitMsg对象
class RecruitComment(models.Model):
    # 简历关连到ResumeMsg
    resume = models.ForeignKey(RecruitMsg)
    # 评论用户，默认不可为空
    person_id = models.IntegerField(verbose_name='发布人ID', null=False, blank=False)
    person_name = models.CharField(verbose_name='姓名', max_length=30, blank=False)
    # 评论时间
    comment_time = models.DateTimeField(verbose_name='评论时间', null=False, blank=False)
    # 评论内容
    comment_content = models.TextField(verbose_name='评论内容', blank=False)

    def __unicode__(self):
        return self.person_name + '的评论'


# 面试交流贴，一个贴子对应一个Interview对象
class Interview(models.Model):
    # 面试交流发布人，默认不可为空
    person_id = models.IntegerField(verbose_name='发布人ID', null=False, blank=False)
    person_name = models.CharField(verbose_name='发布人', max_length=30, blank=False)
    # 标题
    interview_title = models.CharField(verbose_name='标题', max_length=100, blank=False)
    # 面试企业
    interview_company = models.CharField(verbose_name='面试企业', max_length=30, blank=False)
    # 面试时间
    interview_time = models.DateTimeField(verbose_name='面试时间', null=False, blank=False)
    # 面试方式 (电话面试，现场面试，视频面试等)可为空
    interview_way = models.CharField(verbose_name='面试方式', max_length=30, blank=True, choices=(
        ('1', '电话面试'),
        ('2', '现场面试'),
        ('3', '视频面试'),
    ))
    # 面试类别（技术一面，技术二面，HR面等），可为空
    interview_class = models.CharField(verbose_name='面试类别', max_length=30, blank=True, choices=(
        ('1', '一面'),
        ('2', '二面'),
        ('3', '三面'),
        ('4', '四面'),
        ('5', 'HR面'),
        ('6', '不知道第几面'),
    ))
    # 面试内容整理
    interview_content = models.TextField(verbose_name='内容整理', blank=False)

    def __unicode__(self):
        return self.person_name + self.interview_company + '面试总结'


# 最新动态表，每当产生一条新动态的时候向该表中写入一条记录
# 新动态暂定为以下几种情况：
# 1.上传一份新简历
# 2.发布了一条新的招聘动态信息
# 3.发布了一条新的面试经历
class News(models.Model):
    # 新动态产生者，默认不可为空
    person_id = models.IntegerField(verbose_name='发布人ID', null=False, blank=False)
    person_name = models.CharField(verbose_name='发布人', max_length=30, blank=False)
    # 动态标题，默认不可为空
    news_title = models.CharField(verbose_name='动态标题', max_length=50, blank=False)
    # 动态产生时间，默认不可为空
    news_time = models.DateTimeField(verbose_name='动态产生时间', null=False, blank=False)
    # 查看详情地址
    # TODO：这块儿好像可以使用一个统一的接口，通过news的ID值来确定详情页面的地址？先留着吧，应该还是需要这个字段
    news_url = models.URLField(verbose_name='URL', blank=False)


# 招聘日历事件表，当有新事件增加时，向该表中写入一条记录
# 设计方案是不在此处做权限限制，任何平台用户都可以在这个日历里增加事件，人多力量大，光靠一个管理员来增加信息费力又闭塞
class Calendar(models.Model):
    # 新事件产生者，默认不可为空
    # 不过设计任何人都可以在日历中增加公共事项，该字段仅在后台保存备份，不予前端展示
    person_id = models.IntegerField(verbose_name='发布人ID', null=False, blank=False)
    person_name = models.CharField(verbose_name='发布人', max_length=30, blank=False)
    # 招聘事件标题
    event_title = models.CharField(verbose_name='事件标题', max_length=50, blank=False)
    # 招聘事件开始时间
    event_starttime = models.DateTimeField(verbose_name='开始时间', null=False, blank=False)
    # 招聘事件结束时间
    event_endtime = models.DateTimeField(verbose_name='结束时间', null=False, blank=False)
    # 是否为全天事件，目前并没有设计到具体一天中的时间，所以都为全天事件，默认值设为True
    # 考虑到以后可以加入到具体几点有面试，精确到几小时的时候这一字段应该有用，故保留
    event_allday = models.BooleanField(verbose_name='全天事件', default=True, blank=False)
    # 事件在前端展示时的背景颜色
    event_bgcolor = models.CharField(verbose_name='背景颜色', max_length=10, blank=False)
    # 事件是否被删除，前端删除时实为软删除操作，通过字段在后台予以标记，并非真正在后台执行删除操作
    # 默认为True，即可用，值为False时表示不可用
    is_avaliable = models.BooleanField(verbose_name='是否可用', default=True)

