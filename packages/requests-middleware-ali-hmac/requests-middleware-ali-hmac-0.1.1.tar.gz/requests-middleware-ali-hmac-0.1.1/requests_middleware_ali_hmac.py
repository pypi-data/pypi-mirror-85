# encoding=utf-8
import base64
import datetime
import hmac
import sys
from hashlib import sha1
# Syntax sugar.
import pytz

_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)
if is_py3:
    from urllib.parse import parse_qsl, ParseResult
if is_py2:
    from urlparse import ParseResult, parse_qsl

import requests
import ulid2
from requests.compat import quote, urlparse
from requests_middleware import BaseMiddleware


class AliHmacGenerate(BaseMiddleware):

    def __init__(self, AccessKeyId, Secret):
        """
        :param AccessKeyId 公钥 str:
        :param Secret 私匙 str:
        """
        if not isinstance(AccessKeyId, str):
            raise TypeError("AccessKeyId must be str not %s!" % type(AccessKeyId))
        if not isinstance(Secret, str):
            raise TypeError("Secret must be str not %s!" % type(AccessKeyId))
        if len(AccessKeyId.strip()) < 1:
            raise ValueError("AccessKeyId not ''!")
        if len(AccessKeyId.strip()) < 1:
            raise ValueError("Secret not ''!")
        self.__AccessKeyId = AccessKeyId
        self.__Secret = Secret

    """
    不允许随意更改或操作AccessKeyId和Secret.
    """

    @property
    def access_key_id(self):
        return self.__AccessKeyId

    @property
    def secret(self):
        return self.__Secret

    @staticmethod
    def percent_encode(string):
        """
        url 编码
        :param string str:
        :return str:
        """
        if not isinstance(string, str):
            raise TypeError("encode text must be str not %s!" % type(string))
        if len(string.strip()) < 1:
            raise ValueError("encode text must be str not ''!")
        res = quote(string, '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    @staticmethod
    def connection_params(parse_result, AccessKeyId):
        """
        解析url返回params和params_string
        :param parse_result Union[ParseResult, ParseResultBytes]:
        :param AccessKeyId str:
        :return Dict[str, str], str:
        """
        if not isinstance(parse_result, ParseResult):
            raise TypeError("AccessKeyId must be ParseResult not %s!" % type(parse_result))
        if not isinstance(AccessKeyId, str):
            raise TypeError("Secret must be str not %s!" % type(AccessKeyId))
        if len(AccessKeyId.strip()) < 1:
            raise ValueError("AccessKeyId not ''!")

        params = dict(parse_qsl(parse_result.query))
        # 拼装+计算
        # 根据当前时区计算出格林尼治标准时间
        now = datetime.datetime.now(pytz.utc)
        params["AccessKeyId"] = AccessKeyId
        # 哈希方式
        params["SignatureMethod"] = "HMAC-SHA1"
        params["Timestamp"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        params["SignatureVersion"] = "1.0"
        params["SignatureNonce"] = ulid2.generate_ulid_as_base32(now)
        if is_py2:
            params["SignatureNonce"] = params["SignatureNonce"].encode()
        # 排序参数
        items = sorted([(key.strip(), AliHmacGenerate.percent_encode(value.strip())) for key, value in
                        params.items()])
        # 拼装参数
        params_string = "&".join(["=".join(item) for item in items])
        return params, params_string

    def generate_sign(self, params_string, method):
        """
        生成 sign
        :param params_string str:
        :param method str:
        :return str:
        """
        if not isinstance(params_string, str):
            raise TypeError("params_string must be str not %s!" % type(params_string))
        if params_string == "":
            raise ValueError("params_string not ''!")
        if not isinstance(method, str):
            raise TypeError("method must be str not %s!" % type(method))

        signature_string = method + "&%2F&" + self.percent_encode(params_string)
        # 生成盐值
        key = self.secret + "&"
        # 计算hmac
        new = hmac.new(key.encode(), digestmod=sha1)
        new.update(signature_string.encode())
        sign = base64.urlsafe_b64encode(new.digest()).decode()
        return sign

    def before_send(self, request, *args, **kwargs):
        """
        钩子函数 发送之前调用 自动计算sign
        :param request requests.models.PreparedRequest:
        :param args:
        :param kwargs:
        :return:
        """
        if not isinstance(request, requests.models.PreparedRequest):
            raise TypeError("not allow requests type")
        if request.method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
            return
        url = request.url
        if len(url.strip()) < 1:
            raise ValueError("url is not ""!")

        # 解析url
        parse_result = urlparse(url)
        # 解析参数
        params, params_string = self.connection_params(parse_result, self.access_key_id)
        # 生成signtrue
        sign = self.generate_sign(params_string, request.method)
        params["Signature"] = sign
        # 拼接 params
        params_str = "?" + "&".join(["{0}={1}".format(k, v) for k, v in params.items()])
        request.url = parse_result.scheme + "://" + parse_result.hostname + parse_result.path + params_str
