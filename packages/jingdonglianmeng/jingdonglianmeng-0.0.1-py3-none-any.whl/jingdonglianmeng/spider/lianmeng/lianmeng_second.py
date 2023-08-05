# -*- coding: utf-8 -*-
"""京东联盟商品第二步"""


class LianMengTwo(object):

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.start_url = "https://item-soa.jd.com/getWareBusiness?skuId={}"
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
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
            "proxies": "",
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
