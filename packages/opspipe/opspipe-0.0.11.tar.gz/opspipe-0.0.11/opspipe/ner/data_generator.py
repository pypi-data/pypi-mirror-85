# -*- coding: utf-8 -*-
'''
数据生成器
'''
import json
from tqdm import tqdm
from pathlib import Path
from loguru import logger
from theta.utils import load_json_file, split_train_eval_examples
from theta.modeling import LabeledText, load_ner_examples, load_ner_labeled_examples

def train_data_generator(args):
    lines = load_json_file(args.train_file)

    for i, x in enumerate(tqdm(lines)):
        guid = str(i)
        text = x['originalText']
        sl = LabeledText(guid, text)

        entities = x['entities']
        for entity in entities:
            start_pos = entity['start_pos']
            end_pos = entity['end_pos'] - 1
            category = entity['label_type']
            mention = entity['mention']

            # 矫正前后带空格
            ent = text[start_pos:end_pos + 1]
            if mention != ent:
                print('###', mention, ent)
            if len(ent.lstrip()) != len(ent):
                l = len(ent) - len(ent.lstrip())
                start_pos = start_pos + l
                logger.warning(f'{ent} --lstrip-- {text[start_pos:end_pos + 1]}')

            if len(ent.rstrip()) != len(ent):
                l = len(ent) - len(ent.rstrip())
                end_pos = end_pos - l
                logger.warning(f'{ent} --rstrip-- {text[start_pos:end_pos + 1]}')

            if category not in args.ner_labels:
                continue

            sl.add_entity(category, start_pos, end_pos)

        yield str(i), text, None, sl.entities


'''
def load_train_val_examples(args):

    allow_overlap = args.allow_overlap
    if args.num_augements > 0:
        allow_overlap = False

    lines = []
    for guid, text, _, entities in train_data_generator(args.train_file):
        sl = LabeledText(guid, text, entities)
        lines.append({'guid': guid, 'text': text, 'entities': entities})



    logger.info(f"Loaded {len(train_examples)} train examples, "
                f"{len(val_examples)} val examples.")
    return train_examples, val_examples 
'''

def load_train_val_examples(args):
    lines = []
    for guid, text, _, entities in train_data_generator(args.train_file):
        sl = LabeledText(guid, text, entities)
        lines.append({'guid': guid, 'text': text, 'entities': entities})

    allow_overlap = args.allow_overlap
    if args.num_augements > 0:
        allow_overlap = False

    train_base_examples = load_ner_labeled_examples(
        lines,
        args.ner_labels,
        seg_len=args.seg_len,
        seg_backoff=args.seg_backoff,
        num_augements=args.num_augements,
        allow_overlap=allow_overlap)

    train_examples, val_examples = train_base_examples, []
    # 如果训练集和验证集一样就自动切分
    if args.train_file == args.eval_file:
        train_examples, val_examples = split_train_eval_examples(
            train_base_examples,
            train_rate=args.train_rate,
            fold=args.fold,
            shuffle=False)
    else:
        lines = []
        for guid, text, _, entities in train_data_generator(args.eval_file):
            sl = LabeledText(guid, text, entities)
            lines.append({'guid': guid, 'text': text, 'entities': entities})

        val_examples = load_ner_labeled_examples(
            lines,
            args.ner_labels,
            seg_len=args.seg_len,
            seg_backoff=args.seg_backoff,
            num_augements=args.num_augements,
            allow_overlap=allow_overlap)

    logger.info(f"Loaded {len(train_examples)} train examples, "
                f"{len(val_examples)} val examples.")
    return train_examples, val_examples


def test_data_generator(test_file):
    lines = load_json_file(test_file)
    for i, s in enumerate(tqdm(lines)):
        i = s['uid']
        guid = str(i)
        text_a = s['originalText']

        yield guid, text_a, None, None


def load_test_examples(args):
    test_base_examples = load_ner_examples(test_data_generator,
                                           args.test_file,
                                           seg_len=args.seg_len,
                                           seg_backoff=args.seg_backoff)

    logger.info(f"Loaded {len(test_base_examples)} test examples.")
    return test_base_examples

def generate_submission(args):
    reviews_file = f"{args.latest_dir}/{args.dataset_name}_reviews_{args.local_id}.json"
    reviews = json.load(open(reviews_file, 'r'))

    submission_file = f"{args.submissions_dir}/{args.dataset_name}_submission_{args.local_id}.json.txt"
    with open(submission_file, 'w') as wt:
        for guid, json_data in reviews.items():
            output_data = {'originalText': json_data['text'], 'entities': []}
            for json_entity in json_data['entities']:
                output_data['entities'].append({
                    'label_type':
                        json_entity['category'],
                    'overlap':
                        0,
                    'start_pos':
                        json_entity['start'],
                    'end_pos':
                        json_entity['end'] + 1,
                    'mention':
                        json_entity['mention']
                })
            output_data['entities'] = sorted(output_data['entities'],
                                             key=lambda x: x['start_pos'])
            output_string = json.dumps(output_data, ensure_ascii=False)
            wt.write(f"{output_string}\n")

    logger.info(f"Saved {len(reviews)} lines in {submission_file}")

def to_poplar(args):
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
    label2id = {x: i for i, x in enumerate(args.ner_labels)}
    label_categories = poplar_json['labelCategories']
    for _id, x in enumerate(args.ner_labels):
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
    for guid, text, _, entities in train_data_generator(args.train_file):
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
