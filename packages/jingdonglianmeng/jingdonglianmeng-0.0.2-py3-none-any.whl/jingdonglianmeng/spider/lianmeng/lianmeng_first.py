# -*- coding: utf-8 -*-
"""京东联盟商品第一步"""
from urllib.parse import parse_qsl, urlparse


class LianMengOne(object):

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.category_url = "https://union.jd.com/proManager/index?categoryId=1320&sortName=inOrderCount30Days&sort=desc"
        self.start_url = "https://union.jd.com/api/goods/search"
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        }
        super(LianMengOne, self).__init__()

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
        # 从category_url解析出需要用到的参数
        params_data = dict(parse_qsl(urlparse(self.category_url).query, keep_blank_values=True))
        json_data = {
            "pageNo": 1,
            "pageSize": 60,
            "data": params_data
        }
        # post
        kwargs = {
            "url": self.start_url,
            "method": "post",
            "headers": self.headers,
            "proxies": "",
            "session": False,
            "json": json_data,
        }

        return kwargs

    def check_response(self, response):
        """
        检查响应是否正确
        :param response: 响应体
        :return:
        """
        if response.status_code == 200:
            if response.json().get("code") == 200:
                print("请求成功")
                return True

        return False

    def parse_response(self, response):
        """
        解析响应结果,获取所需字段
        :return:
        """
        res_json = response.json()
        data_list = res_json.get("data", {}).get("unionGoods", [])
        for data in data_list:
            skuId = data[0].get("skuId")  # 商品对应id
            skuName = data[0].get("skuName")  # 商品标题
            shopName = data[0].get("shopName")  # 店铺名称
            self.params.update({
                "skuId": skuId,
                "skuName": skuName,
                "shopName": shopName,
            })

            yield self.params
