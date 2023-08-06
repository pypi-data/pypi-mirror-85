# -*- coding: utf-8 -*-
"""京东联盟商品第一步"""
from urllib.parse import parse_qsl, urlparse


class LianMengOne(object):

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.start_url = "https://union.jd.com/api/goods/search"
        self.headers = {
            'cookie': 'thor=90CEC7A0E588FF207139503BF0056761801C5F1B4029EFE863207F36444BEC6DDB8933A926F3DE3D33466D1F2C11ADE850DCC6BA96040B6EC80A52141B58E397F7B29B3F2B48CA7E3665640F57BB85897C7AE775B7099377B65225E1051026DECD0D95D3A42824574473B3ED9A660AC8F93B89260CB56AD34977D33B70E42FC5CDAAE904572791F2FEB3CD72D16F4740E6526A867BCAE72E632DEFE31E67EF82;pin=jd_4517f39da4099',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
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
        url = self.params.get("url")
        # 从category_url解析出需要用到的参数
        params_data = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
        pageNo = params_data.pop("pageNo")
        json_data = {
            "pageNo": int(pageNo),
            "pageSize": 60,
            "data": params_data
        }
        # post
        kwargs = {
            "url": self.start_url,
            "method": "post",
            "headers": self.headers,
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
