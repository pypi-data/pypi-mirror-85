# -*- coding: utf-8 -*-
import re
from ..reg import RegularExtrator as pre

class RegularExtrator(pre):

    def __init__(self, text='',data_list = []):
        pre.__init__(self, text, data_list)  
        self.text = text
        self.data_list = data_list
        
    def clear_list(self,pattern = r'[\s]*'):
        # 去除空格换行符等字符的txt文本列表
        data_list = self.flatten(self.data_list)
        data_list_out = []
        for item in data_list: 
            txt_drop = re.sub(pattern, '', item)       # 清除换行,制表,空格
            data_list_out.append(txt_drop)
        self.data_list = data_list_out
        return self.data_list 
    
    def clear_txt(self,pattern = r'[\s]*'):
        # 去除空格换行符等字符的txt文本列表  
        txt_drop = re.sub(pattern, '', self.text)       # 清除换行,制表,空格 
        self.text = txt_drop
        return txt_drop 
