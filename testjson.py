#!/usr/bin/env python3
# -*- coding：utf-8 -*-

import json

#d = dict(name='Bob', age=20, score=88)
#j = json.dumps(d)
#print (j)

# Python 字典类型转换为 JSON 对象
data = {
    'no' : 1,
    'name': 'sandy',
    'url' : 'http://www.sandy.com',
    "address": {
        "street": "科技园路.",
        "city": "江苏苏州",
        "country": "中国"
    },
    "links": [
        {
            "name": "Google",
            "url": "http://www.google.com"
        },
        {
            "name": "Baidu",
            "url": "http://www.baidu.com"
        },
        {
            "name": "SoSo",
            "url": "http://www.SoSo.com"
        }
    ]
}

json_str = json.dumps(data)
print ("Python 原始数据：", repr(data))
print ("JSON 对象：", json_str)

# 将 JSON 对象转换为 Python 字典
data2 = json.loads(json_str)
print ("data2['name']: ", data2['name'])
print ("data2['address']: ", data2['address'])
print ("data2['links']: ", data2['links'])