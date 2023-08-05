# -*- coding: utf-8 -*-
"""抖音粉丝数第五步"""


class DouYinFive(object):

    def __init__(self, *args, **kwargs):
        self.start_url = "https://v.jingdonglianmeng.com/JMEYBmB/"
        self.headers = {
            'accept-encoding': 'deflate',
            'accept-language': 'zh-CN,zh;q=0.9',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        }
        super(DouYinFive, self).__init__()

    def get_token(self):
        """
        获取渠道所需auth或cookie
        :return:
        """
        return ""

    def structure_params(self, params={}):
        """
        构造参数&请求url
        :param params: 请求需要的参数
        :return:
        """
        # get
        kwargs = {
            "url": self.start_url,
            "method": "get",
            "headers": self.headers,
            "proxies": "",
            "session": False,
            "params": {},
        }
        # # post
        # kwargs = {
        #     "url": self.start_url,
        #     "method": "post",
        #     "headers": self.headers,
        #     "proxies": "",
        #     "data": {},
        #     "json": {},
        # }
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

    def parse_response(self):
        """
        解析响应结果,获取所需字段
        :return:
        """
        # 最后一步解析到需求字段后将最终结构体&映射model一起返回
        return
