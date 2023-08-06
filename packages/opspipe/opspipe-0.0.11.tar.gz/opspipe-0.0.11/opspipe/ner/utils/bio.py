#!/usr/bin/env python
# -*- coding: utf-8 -*-
from theta.utils import load_json_file,seg_generator
from tqdm import tqdm
import random,os
from pathlib import Path
from pipeline.utils import clean_text

def theta2bio(data_root,output_dir,maxlen=512,seg_backoff=128,train_rate=0.9,
              theta_train_file = 'train_data.txt',
              bio_train_file='bio_data.train',bio_dev_file='bio_data.dev'):
    train_file = os.path.join(data_root, theta_train_file)
    train_txts = load_json_file(train_file)
    # lines = train_txts + val_txts

    train = open(Path(output_dir, bio_train_file), 'w', encoding='UTF-8')
    val = open(Path(output_dir, bio_dev_file), 'w', encoding='UTF-8')
    train_txts, val_txts = split_datas(train_txts, True,train_rate)
    create_data(train_txts, train,maxlen,seg_backoff)
    create_data(val_txts, val,maxlen,seg_backoff)

    train.close()
    val.close()


def split_datas(full_list,shuffle=False,train_rate=0.9):
    n_total = len(full_list)
    offset = int(n_total * train_rate)
    if n_total==0 or offset<1:
        return [],full_list
    if shuffle:
        random.shuffle(full_list)
        sublist_1 = full_list[:offset]
        sublist_2 = full_list[offset:]
        return sublist_1,sublist_2

def create_data(lines, w,maxlen=512,seg_backoff=128):
    for i, x in enumerate(tqdm(lines)):
        # guid = str(i)
        text = clean_text(x['originalText'])
        entities = x['entities']
        labels = []
        for entity_json in entities:
            start_pos = entity_json['start_pos']
            end_pos = entity_json['end_pos']
            category = entity_json['label_type']
            # 矫正前后带空格
            # entity = text[start_pos:end_pos]
            labels.append([start_pos, end_pos, category])

        g = seg_generator((text,), maxlen - 2, seg_backoff)
        for t in g:
            text = t[0][0]
            num = t[1]
            stripped_txt = [['O'] * 2 for _ in range(len(text))]
            for i, s in enumerate(text):
                stripped_txt[i][0] = s

            for lable in labels:
                start = lable[0] - num
                end = lable[1] - num
                if start < 0 or end < 0 or start > len(text) or end > len(text):
                    continue

                is_B = True
                for i in range(start, end):
                    if is_B:
                        stripped_txt[i][1] = 'B-' + lable[2]
                        is_B = False
                    else:
                        stripped_txt[i][1] = 'I-' + lable[2]

        for st in stripped_txt:
            output_string = st[0] + ' ' + st[1]
            w.write(f"{output_string}\n")
        w.write(f"\n")