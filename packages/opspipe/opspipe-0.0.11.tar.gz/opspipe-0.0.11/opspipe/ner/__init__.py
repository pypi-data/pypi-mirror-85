#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from pipeline.data_generator import train_data_generator,load_train_val_examples,test_data_generator,generate_submission
from pipeline.utils import copy_dir
import os,sys
'''
    #当前文件路径
    print(os.path.realpath(__file__))
    #当前文件所在的目录，即父路径
    print(os.path.split(os.path.realpath(__file__))[0])
    #找到父路径下的其他文件，即同级的其他文件
    print(os.path.join(proDir,"config.ini"))
'''

def create_baseline():
    # 当前文件路径
    print(os.path.realpath(__file__))
    # 当前文件所在的目录，即父路径
    print(os.path.split(os.path.realpath(__file__))[0])
    proDir =os.path.split(os.path.realpath(__file__))[0]
    # 找到父路径下的其他文件，即同级的其他文件
    print(os.path.join(proDir, "model"))

    print(sys.argv[0])

#create_baseline()
