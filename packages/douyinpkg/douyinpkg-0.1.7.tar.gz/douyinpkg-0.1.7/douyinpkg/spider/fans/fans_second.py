# -*- coding: utf-8 -*-
"""抖音粉丝数第二步"""
import json


class DouYinTwo(object):

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.ua_headers = {
            'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
        }
        # 粉丝数详情页对应的url
        self.fans_url = 'https://{}/web/api/v2/user/info/?sec_uid={}'
        super(DouYinTwo, self).__init__()

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
        hostname = params.get("hostname")
        sec_uid = params.get("sec_uid")
        self.params = params
        # get
        kwargs = {
            "url": self.fans_url.format(hostname, sec_uid),
            "method": "get",
            "headers": self.ua_headers,
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
        if response.status_code == 200:
            print("请求成功")

        return True

    def parse_response(self, response):
        """
        解析响应结果,获取所需字段
        :return:
        """
        # 解析所需字段数据
        result_data = response.json()
        if result_data.get('status_code', '') != 0:
            message = '请求粉丝详情页失败,result_data:{}'.format(json.dumps(result_data, indent=2))
            print('err_message:{}'.format(message))
            return False

        # 粉丝数
        follower_count = result_data.get('user_info', {}).get('follower_count')
        # 发布视频数
        aweme_count = result_data.get('user_info', {}).get('aweme_count')
        # APP名
        app_name = result_data.get('user_info', {}).get('nickname')

        self.params.update({
            "follower_count": follower_count,
            "aweme_count": aweme_count,
            "app_name": app_name,
        })

        yield self.params
