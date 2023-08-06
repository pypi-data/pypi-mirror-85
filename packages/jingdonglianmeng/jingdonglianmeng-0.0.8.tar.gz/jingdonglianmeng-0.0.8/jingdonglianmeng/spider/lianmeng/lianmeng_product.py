# -*- coding: utf-8 -*-
"""京东联盟商品生产者"""
import math


class LianMengProduct(object):

    def __init__(self, *args, **kwargs):
        self.category_url = "https://union.jd.com/proManager/index?categoryId=1320&sortName=inOrderCount30Days&sort=desc&pageNo={}"

        super(LianMengProduct, self).__init__()

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
        return {}

    def check_response(self, response):
        """
        检查响应是否正确
        :param response: 响应体
        :return:
        """
        return True

    def parse_response(self, response):
        """
        解析响应结果,获取所需字段
        :return:
        """
        total_page = math.ceil(500 / 60)
        for page in range(1, total_page + 1):
            category_url = self.category_url.format(page)

            yield {"url": category_url}
