# -*- coding: utf-8 -*-
"""京东联盟商品第二步"""


class LianMengTwo(object):

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.start_url = "https://item-soa.jd.com/getWareBusiness?skuId={}"
        # 需要带cookie
        self.headers = {
            'cookie': 'thor=90CEC7A0E588FF207139503BF0056761801C5F1B4029EFE863207F36444BEC6D4AF0C3DE6065B8846CDE86BBDBD77B4A9A6B5D3FBA2204DB0A541E66DC7B2EC7233251ECFE39EC52B67AC353334B71F943DB62635CECB52605BF6F729F4B73156666FE74B6DF4CC390FF35B5BACEB38A25BB2CF1E5468E95E783FB0EFFD8196875BBE5C21ACF6FD4E21D1ED0D50465C6F7B826A074077667AFE0E4DF6BA91B24; pin=jd_4517f39da4099',
            'accept-encoding': 'gzip,deflate,br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
        }
        super(LianMengTwo, self).__init__()

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
        skuId = self.params.get("skuId")
        # get
        kwargs = {
            "url": self.start_url.format(skuId),
            "method": "get",
            "headers": self.headers,
            "session": False,
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

        return False

    def parse_response(self, response):
        """
        解析响应结果,获取所需字段
        :return:
        """
        # 获取优惠券&市场价&售价
        res_json = response.json()
        price = res_json.get("price", {}).get("p")  # 售价
        market_price = res_json.get("price", {}).get("op")  # 市场价
        couponInfo = res_json.get("couponInfo", [])  # 优惠券
        coupon_list = []
        for info in couponInfo:
            couponValue = info.get("couponValue", "")  # 折扣
            if not couponValue:
                quota = info.get("quota")  # 满
                discount = info.get("discount")  # 减
                couponValue = "满{}减{}".format(quota, discount)

            coupon_list.append(couponValue)

        self.params.update({
            "price": price,
            "market_price": market_price,
            "coupon_list": coupon_list,
        })

        yield self.params
