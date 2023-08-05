# -*- coding: utf-8 -*-

# 请求模块
request_step = [
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
        "mongodb":
            {
                "host": "47.116.109.99",
                "port": 27017,
                "user_name": "",
                "password": "",
                "db_name": "competitor_test_data",
            },
    },
    {
        "print": {}
    }
]
