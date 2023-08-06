# -*- coding: utf-8 -*-
'''
Created on 2020-9-24
先到标注工具新建类型，导入json，再导出json作为model.json
(TODO 标注工具还无法实现导入，无法固定模板)

@author: zhys513(254851907@qq.com)
'''
import json,os 
from tqdm import tqdm
from pathlib import Path
from theta.utils import load_json_file
from loguru import logger
from ...utils import read_json
from ..data_generator import train_data_generator

def theta_train2poplar(args,train_file = 'train_data.txt'):
    '''theta 训练数据 转 标注
    强绑定theta
    '''
    datasets_path = Path(args.data_dir,args.dataset_name)
    train_file = Path(datasets_path,train_file)
    theta2poplar(datasets_path,train_file)

def theta_submission2poplar(args,submission_file = ''):
    '''theta 结果数据 转 标注
    强绑定theta
    '''
    datasets_path = Path(args.data_dir,args.dataset_name)
    if submission_file :
        submission_file = f"{args.submissions_dir}/{args.dataset_name}_submission_{args.local_id}.json.txt"
    theta2poplar(datasets_path,submission_file)

def theta2poplar(datasets_path,json_file,
                 output_path='poplar_output',
                 model_file='model.json'):
    '''theta 数据 转 标注  model_file 为必传项
    可配置'''
    poplar_output = os.path.join(datasets_path,output_path)
    if not os.path.exists(poplar_output):
        os.mkdir(poplar_output)

    # 标注模板 从模板中定义ID和颜色
    label_modle = read_json(Path(datasets_path, model_file))
    label2id, id2label, id2label_color, categorie2id = {}, {}, {}, {}
    for labelCategorie in label_modle['labelCategories']:
        label2id[labelCategorie['text']] = labelCategorie['id']
        id2label[labelCategorie['id']] = labelCategorie['text']
        id2label_color[labelCategorie['id']] = labelCategorie['color']
    for connectionCategorie in label_modle['connectionCategories']:
        categorie2id[connectionCategorie['text']] = connectionCategorie['id']

    # 获取 theta ner 数据格式
    train_datas = load_json_file(json_file)

    for i, x in enumerate(tqdm(train_datas)):
        guid = str((i + 1) * 10000)
        entities = x['entities']
        originalText = x['originalText']
        poplar_labels = []
        for n, entity in enumerate(entities):
            eid = guid + str(n)
            start_pos = entity['start_pos']
            end_pos = entity['end_pos'] - 1
            category = entity['label_type']
            mention = originalText[start_pos:end_pos]
            entity = {
                "id": eid,
                "categoryId": label2id[category],
                "startIndex": start_pos,
                "endIndex": end_pos + 1,
                "mention":mention
            }
            poplar_labels.append(entity)

        poplar_json = label_modle.copy()
        poplar_json['id'] = guid
        poplar_json['title'] = i
        poplar_json['content'] = originalText
        poplar_json['labels'] = poplar_labels

        with open(Path(poplar_output, guid + '.json'), 'w', encoding='utf-8') as wt:
            output_string = json.dumps(poplar_json, ensure_ascii=False, indent=4)
            wt.write(f"{output_string}\n")

def to_poplar(args,ner_labels):
    '''theta 自带'''
    start_pages = 10
    max_pages = 10
    poplar_json = {
        "content": "",
        "labelCategories": [],
        "labels": [],
        "connectionCategories": [],
        "connections": []
    }

    poplar_colorset = [
        '#007bff', '#17a2b8', '#28a745', '#fd7e14', '#e83e8c', '#dc3545',
        '#20c997', '#ffc107', '#007bff'
    ]
    label2id = {x: i for i, x in enumerate(ner_labels)}
    label_categories = poplar_json['labelCategories']
    for _id, x in enumerate(ner_labels):
        label_categories.append({
            "id": _id,
            "text": x,
            "color": poplar_colorset[label2id[x]],
            "borderColor": "#cccccc"
        })

    poplar_labels = poplar_json['labels']
    poplar_content = ""
    eid = 0
    num_pages = 0
    page_offset = 0
    for guid, text, _, entities in train_data_generator(args.train_file,ner_labels):
        if num_pages < start_pages:
            num_pages += 1
            continue

        page_head = f"\n-------------------- {guid} Begin --------------------\n\n"
        page_tail = f"\n-------------------- {guid} End --------------------\n\n"
        poplar_content += page_head + f"{text}" + page_tail

        for entity in entities:
            poplar_labels.append({
                "id":
                    eid,
                "categoryId":
                    label2id[entity.category],
                "startIndex":
                    page_offset + len(page_head) + entity.start,
                "endIndex":
                    page_offset + len(page_head) + entity.end + 1,
            })
            eid += 1

        num_pages += 1
        if num_pages - start_pages >= max_pages:
            break

        page_offset = len(poplar_content)

    poplar_json["content"] = poplar_content
    poplar_json['labels'] = poplar_labels

    poplar_data_file = Path(args.local_dir,'datasets','poplar_data.json')
    json.dump(poplar_json,
              open(poplar_data_file, 'w'),
              ensure_ascii=False,
              indent=2)
    logger.info(f"Saved {poplar_data_file}")

