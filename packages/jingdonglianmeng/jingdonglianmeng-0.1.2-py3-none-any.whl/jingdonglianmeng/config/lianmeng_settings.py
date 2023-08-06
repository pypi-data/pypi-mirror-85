# -*- coding: utf-8 -*-

# 请求模块
request_step = [
    {
        "LianMengProduct": {
            # 执行模式,往redis推入任务
            "run_mode": "requests",
            # 是否需要auth或cookie
            "need_token": False,
        },
    },
    {
        "LianMengOne": {
            # 执行模式requests/WebDriver
            "run_mode": "requests",
            # 是否需要auth或cookie
            "need_token": False,
        },
    },
    {
        "LianMengTwo": {
            # 执行模式requests/WebDriver
            "run_mode": "requests",
            # 是否需要auth或cookie
            "need_token": False,
        },
    },
    {
        "LianMengThree": {
            # 执行模式requests/WebDriver
            "run_mode": "requests",
            # 是否需要auth或cookie
            "need_token": False,
        },
    },
    {
        "LianMengFour": {
            # 执行模式requests/WebDriver
            "run_mode": "requests",
            # 是否需要auth或cookie
            "need_token": False,
        },
    },
]

# 存储途径
output = [
    {
        "print": {}
    },
    {
        "csv": {
            "file_name": "jingdonglianmeng.csv",
            "csv_header": {'联盟二级类目': 'second_category',
                           '类目': 'belong_category',
                           '链接': 'category_url',
                           '商品标题': 'skuName',
                           '店铺名称': 'shopName',
                           '售卖价格': 'price',
                           '市场价': 'market_price',
                           '优惠券': 'coupon_list',
                           '品牌': 'brand_name',
                           '图片': 'img_info',
                           '总销售': 'comment_count',
                           '链接地址': 'product_url',
                           '商品信息': 'product_info',
                           }
        }
    },
]
