# -*- coding: utf-8 -*-
"""
@author: tusky
@time: 2019/3/4 上午9:55
@desc: E8基础数据接口
"""
try:
    import ujson as json
except ImportError:
    import json
import requests
import time
import hashlib

class _Callable(object):
    def __init__(self, api, attr):
        self._api = api
        self._attrs = [attr, ]

    def __getattr__(self, attr):
        self._attrs.append(attr)
        return self

    def __call__(self, **kw):
        return self._api._request('/'.join(self._attrs), **kw)

class E8Api(object):
    def __init__(self, baseurl, appid, secret, debug=False, timeout=30):
        self._baseurl = baseurl
        if not self._baseurl.endswith("/"):
            self._baseurl += '/'
        self._appid = appid
        self._secret = secret
        self._debug = debug
        self._timeout = timeout

    def _request(self, method, **kwargs):
        url = '%s%s' % (self._baseurl, method)
        kwargs["tm"] = int(time.time())
        if self._debug and 'debug' not in kwargs:
            kwargs['debug'] = 1
        if "appid" not in kwargs:
            kwargs["appid"] = self._appid
        items = ["%s=%s" % item for item in kwargs.items()]
        items.sort()
        s = "&".join(items)
        s += self._secret
        sign = hashlib.new("md5", s.encode("utf-8")).hexdigest()
        kwargs["sign"] = sign
        try:
            req = requests.post(url, data=kwargs,timeout=self._timeout)
        except requests.exceptions.ConnectionError:
            return None
        ret = json.loads(req.text)
        if ret['code'] == 0:
            return ret.get('data',{})
        else:
            return None
        
    def __getattr__(self, attr):
        return _Callable(self, attr)