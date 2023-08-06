# -*- coding: utf-8 -*-
"""京东联盟商品第四步"""
import scrapy


class LianMengFour(object):

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.start_url = "https://item.jd.com/{}.html"
        self.headers = {
            'accept-encoding': 'gzip,deflate,br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
        }
        super(LianMengFour, self).__init__()

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
        self.start_url = self.start_url.format(skuId)
        # get
        kwargs = {
            "url": self.start_url,
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
        # 获取品牌&商品介绍&图片url,此时的响应为html
        res_http_content = scrapy.Selector(text=response.content)
        # 品牌名
        brand_name = res_http_content.xpath("//ul[@id='parameter-brand']/li/@title").extract_first()
        # 商品介绍
        product_info = {}
        li_list = res_http_content.xpath("//ul[@class='parameter2 p-parameter-list']/li")
        for li in li_list:
            li_str = li.xpath("./text()").extract_first()
            # 以：进行切割,拆分键值
            info = li_str.split("：")
            product_key = info[0]
            product_value = info[1]
            product_info[product_key] = product_value
        # 图片集
        img_info = []
        img_list = res_http_content.xpath("//div[@id='spec-list']/ul[@class='lh']/li")
        for img in img_list:
            img_url = img.xpath("./img/@src").extract_first()
            if not img_url.startswith('http'):
                img_url = 'http:' + img_url
            img_info.append(img_url)

        result_data = {
            "second_category": self.params.get("second_category"),  # 二级类目
            "belong_category": self.params.get("belong_category"),  # 所属类目
            "category_url": self.params.get("category_url"),  # 需求方提供的url
            "product_url": self.start_url,  # 商品详情对应的url
            "skuName": self.params.get('skuName'),  # 标题
            "shopName": self.params.get('shopName'),  # 店铺名称
            "price": self.params.get('price'),  # 售价
            "market_price": self.params.get('market_price'),  # 市场价
            "coupon_list": self.params.get('coupon_list'),  # 优惠券
            "comment_count": self.params.get('comment_count'),  # 销量
            "brand_name": brand_name,  # 品牌名
            "product_info": product_info,  # 商品介绍
            "img_info": img_info,  # 图片集
        }

        yield result_data
