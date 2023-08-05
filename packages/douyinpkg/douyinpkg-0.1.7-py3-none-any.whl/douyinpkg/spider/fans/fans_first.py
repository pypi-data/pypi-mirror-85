# -*- coding: utf-8 -*-
"""抖音粉丝数第一步"""
from urllib import parse


class DouYinOne(object):

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.start_url = "https://v.douyin.com/JMEYBmB/"
        self.headers = {
            'accept-encoding': 'deflate',
            'accept-language': 'zh-CN,zh;q=0.9',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        }
        super(DouYinOne, self).__init__()

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
        # get
        kwargs = {
            "url": self.start_url,
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
        if response.status_code == 302:
            print("请求成功")

        return True

    def parse_response(self, response):
        """
        解析响应结果,获取所需字段
        :return:
        """
        location = response.headers.get('location')
        # 匹配location中的hostname和sec_uid
        hostname, sec_uid = self.parse_url(location)
        self.params.update({
            "hostname": hostname,
            "sec_uid": sec_uid,
            "location": location,
        })

        yield self.params

    def parse_url(self, url):
        """
        提取url中所需参数
        :param url: 解析的url
        :return: 返回参数
        """
        result = parse.urlparse(url)
        query_dict = parse.parse_qs(result.query)
        application = query_dict.get('sec_uid', [])
        hostname = result.hostname
        if not application:
            message = '提取参数失败: {}'.format(url)
            print('err_message:{}'.format(message))
            return False

        return hostname, application[0]
