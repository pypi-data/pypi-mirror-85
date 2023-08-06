# -*- coding: utf-8 -*-
'''
Created on 2020-11-6

@author: zhys513(254851907@qq.com)
'''
import pyotp
totp = pyotp.TOTP("7RNCXIR3M57ZTXVOC4CM5PJAATZIDW6A")
print("Current OTP:", totp.now())