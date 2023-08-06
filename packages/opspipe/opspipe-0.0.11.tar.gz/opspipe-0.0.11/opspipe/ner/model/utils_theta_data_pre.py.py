# -*- coding: utf-8 -*-
'''
Created on 2020-9-29
csv 标注数据转换为 theta ner训练数据
@author: zhys513(254851907@qq.com)
'''
import json, os
from pathlib import Path
from tqdm import tqdm
import pandas as pd
from collections import Counter


def load_txts(filename):
    with open(filename, encoding='utf-8') as f:
        return f.readlines()


def load_txt(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()


data_dir = 'datasets/ccf2020_business_ner'
labels = []
train_data, test_data, txt_list = [], [], []


# 转换 csv 转换预测集时要考虑空的问题
def conver_labels(train_dir):
    # for file in tqdm(list(Path(data_dir, 'train').glob('*.ann'))[:]):
    label_path = Path(data_dir, train_dir, 'label')
    label_list = os.listdir(label_path)
    for file in label_list:
        file_name = str(file).split('.')[0]
        originalText = load_txt(Path(data_dir, train_dir, 'data', file_name + '.txt'))
        # originalText = originalText.replace(' ',',')
        if originalText[:1] == ' ': originalText = '@' + originalText[1:]
        txt_list.append(originalText)
        categorys = pd.read_csv(Path(label_path, file), encoding='UTF-8')  # sep='\t')
        output_data = {'originalText': originalText, 'entities': []}
        for _, row in categorys.iterrows():  # 1001,position,55,60,法国著名歌手
            label_type = row[1]
            start_pos = int(row[2])
            end_pos = int(row[3] + 1)
            mention = str(row[4])
            #if label_type in ['vx', 'QQ']:
            #    start_pos = start_pos - 3

            if mention != originalText[start_pos:end_pos]:
                print(label_type, mention, originalText[int(start_pos):int(end_pos)], file)
                # print(entity,originalText[start_pos:end_pos])
            output_data['entities'].append({
                'label_type': label_type,
                'overlap': 0,
                'start_pos': start_pos,
                'end_pos': end_pos,
                'mention': originalText[start_pos:end_pos]
            })
            labels.append(label_type)
        train_data.append(output_data)

        # 输出theta ner训练数据格式
        # with open(Path(data_dir, "train_data.txt"), 'w', encoding='utf-8') as wt:
        with open(Path(data_dir, train_dir + "_data.txt"), 'w', encoding='utf-8') as wt:
            for output_data in train_data:
                output_string = json.dumps(output_data, ensure_ascii=False)
                wt.write(f"{output_string}\n")


# 为不影响label的生成，需先dev后train
conver_labels('train')
print(Counter(labels))

with open(Path(data_dir, "labels.txt"), 'w', encoding='utf-8') as wt:
    labels = list(set(labels))
    for output_string in labels:
        wt.write(f"{output_string}\n")

# 转换测试数据
with open(Path(data_dir, "test_data.txt"), 'w', encoding='utf-8') as wt:
    for file in tqdm(list(Path(data_dir, 'test').glob('*.txt'))[:]):
        originalText = load_txt(file)
        # originalText = originalText.replace(' ',',')
        if originalText[:1] == ' ': originalText = '@' + originalText[1:]
        txt_list.append(originalText)
        file_name = os.path.basename(file).split('.')[0]
        output_data = {'originalText': originalText, 'uid': file_name}
        output_string = json.dumps(output_data, ensure_ascii=False)
        wt.write(f"{output_string}\n")

txt_list = ['【' + str(len(txt)) + '】' for txt in txt_list]
count = Counter(txt_list)
print(count)

