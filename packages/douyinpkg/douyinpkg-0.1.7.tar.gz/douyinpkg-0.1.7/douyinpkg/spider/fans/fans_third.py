# -*- coding: utf-8 -*-
"""抖音粉丝数第三步"""
import re


class DouYinThree(object):

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.url = None
        self.headers = {
            'accept-encoding': 'deflate',
            'accept-language': 'zh-CN,zh;q=0.9',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        }
        super(DouYinThree, self).__init__()

    def get_token(self):
        """
        获取渠道所需auth或cookie
        :return:
        """
        return ""

    def structure_params(self, params):
        """
        构造参数&请求url
        :param params: 请求需要的参数
        :return:
        """
        self.params = params
        self.url = params.get("location")
        # get
        kwargs = {
            "url": self.url,
            "method": "get",
            "headers": self.headers,
            "proxies": "",
            "session": False,
            "params": {},
        }

        return kwargs

    def check_response(self, response):
        """
        检查响应是否正确
        :param response: 响应体
        :return:
        """
        if response:
            print("请求成功")

        return True

    def parse_response(self, response):
        """
        解析响应结果,获取所需字段
        :return:
        """
        # 正则匹配user_id
        number = re.findall(r'share/user/(\d+)', self.url)
        if not len(number):
            return {}

        user_id = number[0]

        dytk = re.findall("dytk: '(.*)'", response.content.decode('utf-8'))
        if len(dytk):
            dytk = dytk[0]

        self.params.update({
            "dytk": dytk,
            "user_id": user_id,
        })

        yield self.params
