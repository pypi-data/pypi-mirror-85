# -*- coding: utf-8 -*-
'''
Created on 2020-11-9

@author: zhys513(254851907@qq.com)
'''

from opspipe.reg.scanner import regularExtrator
from opspipe.reg.common import regularExtrator as cRegularExtrator
from opspipe.base.logger import logtime 
'''
资质证书名称、企业名称、详细地址、统一社会信用代码、法定代表人、注册资本、经济性质、证书编号、有效期
'''

# 资质证书名称
def get_qualification_certificate(txt): 
    try:
        ex = regularExtrator(txt) 
        ex.split_txt('企业名称:')
        #ex.print_list()
        ex.text = ex.data_list[0]
        ex.clear_txt(r'\n')
    except:
        ex.text = ''
    return ex.text


# 企业名称
def get_enterprise_name(txt):
    try:
        ex = regularExtrator(txt) 
        ex.split_txt('企业名称:')
        #ex.print_list()
        ex.text = ex.data_list[1]
        ex.split_txt('\n')  
        ex.text = ex.data_list[0]
    except:
        ex.text = ''
    return ex.text


# 详细地址
def get_addr_detailed(txt):
    try:
        ex = regularExtrator(txt) 
        ex.split_txt('详细地址:')
        #ex.print_list()
        ex.text = ex.data_list[1]
        ex.split_txt('\n')  
        ex.text = ex.data_list[0]
    except:
        ex.text = ''
    return ex.text

 
# 统一社会信用代码
def get_unified_social_credit_code(txt):
    try:
        ex = regularExtrator(txt) 
        ex.split_txt('法定代表人:')
        ex.text = ex.data_list[0]
        ex.split_txt('\n')  
        #ex.print_list() 
        ex.text = ex.scan_for_lists_p('\d{6}')[0]
        cre = cRegularExtrator(ex.text)
        ex.text = cre.remove_chinese()
        ex.clear_txt() 
    except:
        ex.text = ''
    return ex.text


# 法定代表人
def get_legal_representative(txt):
    try:
        ex = regularExtrator(txt) 
        ex.split_txt('法定代表人:')
        #ex.print_list()
        ex.text = ex.data_list[1]
        ex.split_txt('\n')  
        ex.text = ex.data_list[0]
        ex.clear_txt()
    except:
        ex.text = ''
    return ex.text


# 注册资本
def get_registered_capital(txt):
    try:
        ex = regularExtrator(txt) 
        ex.split_txt('注册资本:')
        #ex.print_list()
        ex.text = ex.data_list[1]
        ex.split_txt('\n')  
        ex.text = ex.data_list[0]
        ex.clear_txt()
    except:
        ex.text = ''
    return ex.text
 
# 经济性质
def get_economic_nature(txt):
    try:
        ex = regularExtrator(txt) 
        ex.split_txt('经济性质:')
        #ex.print_list()
        ex.text = ex.data_list[1]
        ex.split_txt(r'证书编号:')  
        ex.text = ex.data_list[0]
        ex.clear_txt()
    except:
        ex.text = ''
    return ex.text

#证书编号
def get_certificate_number(txt):
    try:
        ex = regularExtrator(txt) 
        ex.split_txt('证书编号:')
        #ex.print_list()
        ex.text = ex.data_list[1]
        ex.split_txt(r'有效期:')  
        ex.text = ex.data_list[0]
        ex.clear_txt()
    except:
        ex.text = ''
    return ex.text

#有效期
def get_validity_date(txt):
    try:
        ex = regularExtrator(txt) 
        ex.split_txt('有效期:')
        #ex.print_list()
        ex.text = ex.data_list[1]
        ex.split_txt(r'发证机关:')  
        ex.text = ex.data_list[0]
        ex.text = ex.split_txt('\n')[0]
        ex.clear_txt()
    except:
        ex.text = ''
    return ex.text


#  发证机关
def get_post_company(txt):
    try:
        ex = regularExtrator(txt) 
        ex.split_txt('发证机关:')  
        ex.text = ex.data_list[1]
        ex.split_txt('\n')  
        ex.data_list = [x for x in ex.data_list if x != '']
        ex.text = ex.data_list[1]
        ex.clear_txt()
    except:
        ex.text = ''
    return ex.text
# 
# # 发证日期
def get_post_date(txt):
    try:
        ex = regularExtrator(txt) 
        ex.split_txt('发证机关')
        #ex.print_list()
        ex.text = ex.data_list[1]
        ex.split_txt(r'有效期:')  
        ex.text = ex.data_list[0]
        cre = cRegularExtrator(ex.text)
        ex.text = cre.extract_date()[0]
        ex.clear_txt()
    except:
        ex.text = ''
    return ex.text 

@logtime
def get_result(txt):
    
    # 资质证书名称
    qualification_certificate = get_qualification_certificate(txt)

    # 企业名称
    enterprise_name = get_enterprise_name(txt)

    # 详细地址
    addr_detailed = get_addr_detailed(txt)
 
    # 统一社会信用代码
    unified_social_credit_code = get_unified_social_credit_code(txt)

    # 法定代表人
    legal_representative = get_legal_representative(txt)

    # 注册资本
    registered_capital = get_registered_capital(txt)
 
    # 经济性质
    economic_nature = get_economic_nature(txt)

    #证书编号
    certificate_number = get_certificate_number(txt)

    #有效期
    validity_date = get_validity_date(txt)
     
    post_company = get_post_company(txt)
    
    post_date = get_post_date(txt)
    
    result = {"qualification_certificate": qualification_certificate,
              "enterprise_name": enterprise_name,
              "addr_detailed": addr_detailed,
              "unified_social_credit_code": unified_social_credit_code,
              "legal_representative": legal_representative,
              "registered_capital": registered_capital,
              "economic_nature": economic_nature,
              "certificate_number": certificate_number, 
              "validity_date": validity_date,
              "post_company": post_company,
              "validity_date": post_date,
              }
 
    return result