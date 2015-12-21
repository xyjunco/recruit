# coding=utf-8
__author__ = 'junco'
__date__ = ''

import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from django.http import HttpResponseRedirect

from settings import JWT_KEY


class Authentication(object):
    def __init__(self):
        pass

    def process_request(self, request):
        try:
            # 从header中解析出bearer字段对应的token值
            # Request对象中对header进行了封装，在解析自定义参数的时候需要加上‘HTTP_’前缀，并且全部为大写
            # 参见https://docs.djangoproject.com/en/1.9/ref/request-response/
            # Any HTTP headers in the request are converted to META keys by converting all characters to uppercase,
            # replacing any hyphens with underscores and adding an HTTP_ prefix to the name.
            # So, for example, a header called X-Bender would be mapped to the META key HTTP_X_BENDER.

            token = request.META['HTTP_BEARER']
            header = jwt.decode(token, JWT_KEY)
            print header

        # token失败
        except DecodeError:
            return HttpResponseRedirect('')

        # token过期
        except ExpiredSignatureError:
            return HttpResponseRedirect('')

        # header中无token
        except KeyError:
            pass
            # return HttpResponseRedirect('http://cs.xiyoulinux.org')

        return None
