# -*- coding: utf-8 -*-
import re 
from .spliter import RegularExtrator as pre

class RegularExtrator(pre):

    def __init__(self, text='',data_list = []):
        pre.__init__(self, text, data_list)  
        self.text = text
        self.data_list = data_list 
    
    '''
      从list中查询包含字符列表的项  多种组合全部满足才匹配成功
    lists:  ['',''],['','']
    '''
    def scan_for_lists(self,*lists:list):
        data_list = self.flatten(self.data_list)
        data_list_out = []
        for item in data_list: 
            mt = True
            for list_p in lists:
                if not any(word in item for word in list_p): 
                    mt = False 
            if mt :
                data_list_out.append(item)
        self.data_list = data_list_out
        return self.data_list 

    '''
      从list中匹配正则列表的项 ,多项正则全部匹配才正确
    '''
    def scan_for_lists_p(self,*patterns:str): 
        data_list = self.flatten(self.data_list)
        data_list_out = []
        for item in data_list: 
            mt = True
            for pattern in patterns:
                match = re.search(pattern, item)
                if not match: 
                    mt = False
            if mt:
                data_list_out.append(item)
        self.data_list = data_list_out
        return self.data_list
    
    '''
    从文本抽取单个
    '''
    def match_txt_o(self,pattern:str): 
        match = re.findall(pattern, self.text)
        if match:
            self.text = match[0]
        else:
            self.text = ''
        return self.text
    
    
    '''
    从文本抽取多个
    '''
    def match_txt_m(self,pattern:str):
        self.data_list = re.findall(pattern, self.text)    
        return self.data_list
    
    '''
    从list抽取单个
    '''
    def match_list_o(self,pattern:str): 
        data_list = self.flatten(self.data_list) 
        for items in data_list:
            match = re.search(pattern, items)
            if match: 
                self.text = match.group()   
            else:
                self.text = '' 
        return self.text
                
    
    '''
    从list抽取多个
    '''
    def match_list_m(self,pattern:str): 
        data_list = self.flatten(self.data_list)
        data_list_out = []
        for item in data_list: 
            match = re.findall(pattern, item)  
            data_list_out = data_list_out + match
        self.data_list = data_list_out
        return self.data_list