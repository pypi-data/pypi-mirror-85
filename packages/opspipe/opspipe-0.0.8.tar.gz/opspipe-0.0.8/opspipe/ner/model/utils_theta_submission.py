# -*- coding: utf-8 -*-
'''
Created on 2020-9-29
csv 标注数据转换为 theta ner训练数据
@author: zhys513(254851907@qq.com)
'''
import json, os,re
from pathlib import Path
from tqdm import tqdm
from ..utils import validateEmail 
import pandas as pd
from collections import Counter
from loguru import logger
 
def generate_submission(args):
    all_ner_labels = []
    reviews_file = f"{args.latest_dir}/{args.dataset_name}_reviews_{args.local_id}.json"
    reviews = json.load(open(reviews_file, 'r', encoding='utf-8'))

    output_datas = []
    submission_file = f"{args.submissions_dir}"

    for guid, json_data in reviews.items():  # T1    DRUG_DOSAGE 111 113    丸剂
        originalText = json_data['text']

        for _, json_entity in enumerate(json_data['entities']):
            # T = 'T' + str(i + 1)
            label_type = json_entity['category']
            start_pos = int(json_entity['start'])
            end_pos = int(json_entity['end'])
            entity = originalText[start_pos:end_pos + 1]

            if 0 < len(entity) and len(entity) < 80:
                output_data = [str(guid), label_type, start_pos, end_pos, '0']
                output_datas.append(output_data)
                all_ner_labels.append(label_type)

    df = pd.DataFrame(output_datas, columns=['﻿ID', 'Category', 'Pos_b', 'Pos_e', 'Privacy'])
    df.to_csv(Path(submission_file, 'predict.csv'), index=None, encoding='UTF-8')

    logger.info(f'Count: {len(output_datas)} {Counter(all_ner_labels)}')

    logger.info(f"Saved {len(reviews)} lines in {submission_file}")

    from theta.modeling import archive_local_model
    archive_local_model(args, submission_file)
 