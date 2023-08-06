# -*- coding: utf-8 -*-
class RegularExtrator_txt():

    def __init__(self, text='',data_list = []):
        self.text = text
      
    def select_txt(self,start_index = 0, end_index = 0): 
        # 文本 范围选取
        txt_len = len(self.text)
        if end_index == 0:
            end_index = txt_len 
        self.text = self.text[start_index:end_index]   
        return self.text
    
    def set_txt(self,txt):
        self.text = txt
        return self  
    
    def print_txt(self,uid='-'):
        print(f'text({uid})>>>',self.text)
           

class RegularExtrator(RegularExtrator_txt):

    def __init__(self, text='',data_list = []):
        RegularExtrator_txt.__init__(self, text)
        self.text = text
        self.data_list = data_list
    
    def select_list(self,start_index = 0, end_index = 0): 
        # list 范围选取
        list_len = len(self.data_list)
        if end_index == 0:
            end_index = list_len 
        self.data_list = self.data_list[start_index:end_index]   
        return self.data_list
      
    def set_list(self,data_list):
        self.data_list = data_list
        return self
     
         
    def print_list(self,uid='-'):
        print(f'list({uid})>>>',self.data_list)
        
    def flatten(self,nested):
        try:
            #不要迭代类似字符串的对象：
            try:
                nested+'' 
            except TypeError:
                pass
            else:
                raise TypeError
    
            for sublist in nested:
                for element in self.flatten(sublist):
                    yield element
        except TypeError:
            yield nested