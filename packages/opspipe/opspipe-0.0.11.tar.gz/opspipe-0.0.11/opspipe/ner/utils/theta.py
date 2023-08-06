# -*- coding: utf-8 -*-
'''
Created on 2020-9-24
先到标注工具新建类型，导入json，再导出json作为model.json

@author: zhys513(254851907@qq.com)
'''
import json,os
from pathlib import Path
from ...utils import read_json

def poplar2theta(poplar_path, output_path, train_file='train_data.txt', labels_file='labels.txt'):
    '''标注数据 转 theta
    可配置'''
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    labels, output_datas = [], []
    poplar_path_name = [[Path(poplar_path, i), i.split('.')[0]] for i in os.listdir(poplar_path) if
                        i.split('.')[-1] == 'json']
    for p, i in poplar_path_name:
        poplar = read_json(p)
        guid = poplar['id']
        originalText = poplar['content']
        title = poplar['title']
        labelCategories_dict = {row['id']: row['text'] for row in poplar['labelCategories']}
        poplars = poplar['labels']
        output_data = {'guid': guid, 'title': title, 'originalText': originalText, 'entities': []}
        for epos in poplars:
            # eid = epos['id']
            categoryId = epos['categoryId']
            start_pos = epos['startIndex']
            end_pos = epos['endIndex']
            label_type = labelCategories_dict[categoryId]
            output_data['entities'].append({
                'label_type': label_type,
                'overlap': 0,
                'start_pos': start_pos,
                'end_pos': end_pos,
                'mention': originalText[start_pos:end_pos]
            })

            labels.append(label_type)

        output_datas.append(output_data)

        with open(Path(output_path, train_file), 'w', encoding='utf-8') as wt:
            for output_data in output_datas:
                output_string = json.dumps(output_data, ensure_ascii=False)
                wt.write(f"{output_string}\n")

    with open(Path(output_path, labels_file), 'w', encoding='utf-8') as wt:
        labels = list(set(labels))
        for output_string in labels:
            wt.write(f"{output_string}\n") 
