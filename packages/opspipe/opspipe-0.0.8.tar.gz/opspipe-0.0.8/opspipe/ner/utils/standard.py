# -*- coding: utf-8 -*-
'''
标准数据格式转换工具
'''
from pathlib import Path
from ...utils import read_json

def get_standard_dict(standard_path,
                      sources_file  = 'sources.json',
                      labels_file ='labels.json',
                      labelCategories = 'labelCategories.json',
                      connections = 'connections.json',
                      connectionCategories = 'connectionCategories.json'):
    '''
    转换标准数据为ID字典
    '''
    sources = read_json(Path(standard_path,sources_file))
    labels = read_json(Path(standard_path,labels_file))
    labelCategories = read_json(Path(standard_path,labelCategories))
    connections = read_json(Path(standard_path,connections))
    connectionCategories = read_json(Path(standard_path,connectionCategories))
    labelCategories_dict = {row['id']:row['text'] for row in labelCategories}
    labels_dict = {str(row['id']*1000) + row['srcId']:{'srcId':row['srcId'],'name':row['name'],'categoryId':row['categoryId'],'startIndex':row['startIndex'],'endIndex':row['endIndex']} for row in labels}
    sources_dict = {row['id']:{'title':row['title'],'content':row['content']} for row in sources}
    connectionCategories_dict = {row['id']:row['text'] for row in connectionCategories}
    return connections,labelCategories_dict,labels_dict,sources_dict,connectionCategories_dict