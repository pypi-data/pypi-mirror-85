# -*- coding: utf-8 -*-
import re 
from .cleaner import RegularExtrator as cre

class RegularExtrator(cre):

    def __init__(self, text='',data_list = []):
        cre.__init__(self, text, data_list)  
        self.text = text
        self.data_list = data_list 
    
    def split_list(self,pattern_split= r'[，。；]'): 
        data_list = self.flatten(self.data_list)
        data_list_out = []
        for item in data_list: 
            txt_split = re.split(pattern_split, item) 
            data_list_out.append(txt_split)
        self.data_list = data_list_out
        return self.data_list
    
    def split_txt(self,pattern_split= r'[，。；]'): 
        data_list_out = re.split(pattern_split, self.text) 
        self.data_list = data_list_out
        return self.data_list

    def seg_generator(self,seg_len, seg_backoff=0):   # 滑窗算法
        data_list_out = []
        iterables = (self.text, )
        if seg_len <= 0:
            #yield iterables, 0
            data_list_out = [self.text]
        else:
            #  # 确保iterables列表中每一项的条目数相同
            #  assert sum([len(x)
            #              for x in iterables]) == len(iterables[0]) * len(iterables)
            assert iterables[0] is not None
            s0 = 0
            while s0 < len(iterables[0]):
                s1 = s0 + seg_len
                segs = [x[s0:s1] if x else None for x in iterables]
                #yield segs, s0
                s0 += seg_len - seg_backoff 
                data_list_out.append(segs[0])
                
        self.data_list = data_list_out
        
        return self.data_list