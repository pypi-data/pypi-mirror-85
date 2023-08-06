#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64


def base64_to_file(decoded_file_name, base64String):
    # 写入文件
    with open(decoded_file_name, 'wb') as f:
        f.write(base64.b64decode(base64String))
        # print ("解码完毕")
 
def base64_to_str(base64String):
    res = base64.b64decode(base64String.encode('utf-8')).decode("utf-8")
    return res
