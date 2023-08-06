# -*- coding: utf-8 -*-
"""京东联盟商品生产者"""
import math


class LianMengProduct(object):

    def __init__(self, *args, **kwargs):
        self.category = [
            {
                "second_category": "美食佳肴",
                "belong_category": "食品饮料",
                "category_url": "https://union.jd.com/proManager/index?categories=1320&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?categoryId=1320&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            },
            {
                "second_category": "四季茗茶",
                "belong_category": "茶",
                "category_url": "https://union.jd.com/proManager/index?keywords=茶&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?key=茶&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            },
            {
                "second_category": "名酒精酿",
                "belong_category": "酒类",
                "category_url": "https://union.jd.com/proManager/index?categories=12259&keywords=酒&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?categoryId=12259&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            },
            {
                "second_category": "办公文创",
                "belong_category": "文创",
                "category_url": "https://union.jd.com/proManager/index?keywords=文创&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?key=文创&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            },
            {
                "second_category": "生活潮品",
                "belong_category": "创意",
                "category_url": "https://union.jd.com/proManager/index?keywords=创意&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?key=创意&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            },
            {
                "second_category": "个护清洁",
                "belong_category": "个护",
                "category_url": "https://union.jd.com/proManager/index?keywords=个护&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?key=个护&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            },
            {
                "second_category": "汉服",
                "belong_category": "汉服",
                "category_url": "https://union.jd.com/proManager/index?keywords=汉服&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?key=汉服&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            },
            {
                "second_category": "时尚穿搭",
                "belong_category": "潮服",
                "category_url": "https://union.jd.com/proManager/index?keywords=潮服&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?key=潮服&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            },
            {
                "second_category": "时尚穿搭",
                "belong_category": "鞋",
                "category_url": "https://union.jd.com/proManager/index?keywords=鞋子&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?key=鞋子&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            },
            {
                "second_category": "箱包用具",
                "belong_category": "旅行箱",
                "category_url": "https://union.jd.com/proManager/index?keywords=旅行箱&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?key=旅行箱&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            },
            {
                "second_category": "箱包用具",
                "belong_category": "包",
                "category_url": "https://union.jd.com/proManager/index?keywords=包&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?key=包&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            },
            {
                "second_category": "美容护肤/香水彩妆",
                "belong_category": "美妆护肤",
                "category_url": "https://union.jd.com/proManager/index?categories=1316&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?categoryId=1316&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            }, {
                "second_category": "3C数码",
                "belong_category": "数码配件",
                "category_url": "https://union.jd.com/proManager/index?categoryId=652&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?categoryId=652&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            },
            {
                "second_category": "家用电器",
                "belong_category": "家用电器",
                "category_url": "https://union.jd.com/proManager/index?categoryId=737&sortName=inOrderCount30Days&pageNo=1&sort=desc",
                "url": "https://union.jd.com/proManager/index?categoryId=737&sortName=inOrderCount30Days&pageNo={}&sort=desc",
            },

        ]

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
        for category in self.category:
            for page in range(1, total_page + 1):
                url = category.get("url").format(page)
                params = {
                    "second_category": category.get("second_category"),
                    "belong_category": category.get("belong_category"),
                    "category_url": category.get("category_url"),
                    "url": url,
                }

                yield params
