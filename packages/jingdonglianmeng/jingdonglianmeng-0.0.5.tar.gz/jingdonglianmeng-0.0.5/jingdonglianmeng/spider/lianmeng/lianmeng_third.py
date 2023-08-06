# -*- coding: utf-8 -*-
"""京东联盟商品第三步"""


class LianMengThree(object):

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.start_url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}"
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
        }
        super(LianMengThree, self).__init__()

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
        # 获取评论数
        res_json = response.json()
        CommentsCount = res_json.get("CommentsCount", [])
        if not CommentsCount:
            print("该商品没有评论数")
            comment_count = 0
        else:
            comment_count = CommentsCount[0].get('CommentCount')  # 评论总数/销量

        self.params.update({
            "comment_count": comment_count,
        })

        yield self.params
