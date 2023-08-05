#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : padding
# @Time         : 2020-04-10 14:11
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

from sklearn.utils.murmurhash import murmurhash3_32

def murmurhash(key="key", value="value", bins=10000):
    hashValue = murmurhash3_32(f"{key}:{value}")
    return abs(hashValue) % bins


print(murmurhash())
