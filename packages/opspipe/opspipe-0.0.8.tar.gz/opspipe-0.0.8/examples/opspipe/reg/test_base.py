# -*- coding: utf-8 -*-
'''
Created on 2020-11-9

@author: zhys513(254851907@qq.com)
'''
from opspipe.reg.common import regularExtrator
from unittest import TestCase 
import unittest

text = '急寻特朗普，男孩，于2018年11月27号11时在陕西省安康市汉滨区走失。丢失发型短发，...如有线索，请迅速与警方联系：系18100065143，132-6156-2938，baizhantang@sina.com.cn 和yangyangfuture at gmail dot com'
    
class TestMain(TestCase):
    
    def test_set_txt(self): 
        ex = regularExtrator(text)  
        ex.print_txt()
        ex.set_txt('0000').print_txt()
        self.assertEqual(ex.text,'0000')

if __name__ == "__main__": 
    unittest.main()
     
 
    
    