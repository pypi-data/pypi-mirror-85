# -*- coding: utf-8 -*-

# 请求模块
request_step = [
    {
        "DouYinOne": {
            # 执行模式requests/WebDriver
            "run_mode": "requests",
            # 是否需要auth或cookie
            "need_token": False,
        },
    },
    {
        "DouYinTwo": {
            # 执行模式requests/WebDriver
            "run_mode": "requests",
            # 是否需要auth或cookie
            "need_token": False,
        },
    },
    {
        "DouYinThree": {
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
