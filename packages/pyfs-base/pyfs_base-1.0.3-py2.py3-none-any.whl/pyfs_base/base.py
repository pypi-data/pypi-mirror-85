# -*- coding: utf-8 -*-

import json

import requests
from pywe_xml import dict_to_xml


class BaseFeishu(object):
    def __init__(self):
        self.OPEN_DOMAIN = 'https://open.feishu.cn'

    def geturl(self, url, **kwargs):
        return url.format(**kwargs)

    def get(self, url, verify=False, encoding='utf-8', res_to_encoding=True, res_to_json=True, res_processor_func=None, resjson_processor_func=None, authorization=True, authorization_key='token', **kwargs):
        # When ``verify=True`` and ``cacert.pem`` not match ``https://xxx.weixin.qq.com``, will raise
        # SSLError: [Errno 1] _ssl.c:510: error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed
        if kwargs and authorization and isinstance(kwargs, dict) and kwargs.get(authorization_key):
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {0}'.format(kwargs.get(authorization_key)),
            }
            res = requests.get(url.format(**kwargs), headers=headers, verify=verify)
        else:
            res = requests.get(url.format(**kwargs), verify=verify)
        if res_to_encoding:
            res.encoding = encoding
        if res_processor_func:
            return res_processor_func(res)
        if not res_to_json:
            return res
        resjson = res.json()
        return resjson_processor_func(resjson) if resjson_processor_func else resjson

    def post(self, url, verify=False, encoding='utf-8', data_to_json_str=True, data_to_xml_str=False, res_to_encoding=True, res_to_json=True, res_processor_func=None, resjson_processor_func=None, authorization=True, authorization_key='token', **kwargs):
        # https://github.com/requests/requests/blob/9dd823c289faca0d496ef71f25d36216d2259ca3/requests/models.py#L87
        # if (not files):
        #     raise ValueError("Files must be provided.")
        # elif isinstance(data, basestring):
        #     raise ValueError("Data must not be a string.")
        if not kwargs.get('files', None):
            data = kwargs.get('data', None)
            if data:
                if authorization and isinstance(data, dict) and data.get(authorization_key):
                    kwargs['headers'] = {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer {0}'.format(data.get(authorization_key)),
                    }
                if data_to_json_str and isinstance(data, dict):
                    if not kwargs.get('headers'):
                        kwargs['headers'] = {
                            'Content-Type': 'application/json',
                        }
                    kwargs['data'] = json.dumps(data, ensure_ascii=False).encode('utf-8')
                if data_to_xml_str and isinstance(data, dict):
                    kwargs['data'] = dict_to_xml(data)
        res = requests.post(url, verify=verify, **kwargs)
        if res_to_encoding:
            res.encoding = encoding
        if res_processor_func:
            return res_processor_func(res)
        if not res_to_json:
            return res
        resjson = res.json()
        return resjson_processor_func(resjson) if resjson_processor_func else resjson
