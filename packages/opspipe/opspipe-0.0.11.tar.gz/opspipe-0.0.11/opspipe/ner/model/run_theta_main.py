#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 nohup python run_task5.py --do_experiment --data_dir data > logs/log.log 2>&1 &
'''
import os, sys, json, random, copy
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import os, sys
from collections import Counter
import pandas as pd
from tqdm import tqdm
from loguru import logger
from theta.utils import load_json_file, split_train_eval_examples
from theta.modeling import LabeledText, load_ner_examples, load_ner_labeled_examples, save_ner_preds, show_ner_datainfo
from pathlib import Path
import utils_theta_submission
from pipeline.utils import read_txts

#  if os.environ['NER_TYPE'] == 'span':
#      from theta.modeling.ner_span import load_model, get_args
#  else:
#      from theta.modeling.ner import load_model, get_args

dataset_dir = 'datasets'
dataset_name = 'ccf2020_business_ner'
#read_txts(Path(dataset_dir,dataset_name,'labels.txt'))
ner_labels =[
    'game',
    'scene',
    'vx',
    'name',
    'company',
    'organization',
    'mobile',
    'movie',
    'email',
    'QQ',
    'government',
    'position',
    'book',
    'address'
    ]

# -------------------- Data --------------------

def clean_text(text):
    text = str(text).replace('\n',' ')
    # if text:
    #    text = text.strip()
    # text = re.sub('\n', ' ', text)
    return text

def train_data_generator(train_file):
    lines = load_json_file(train_file)

    for i, x in enumerate(tqdm(lines)):
        guid = str(i)
        text = clean_text(x['originalText'])
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
                print(ent, '--lstrip--', text[start_pos:end_pos + 1])

            if len(ent.rstrip()) != len(ent):
                l = len(ent) - len(ent.rstrip())
                end_pos = end_pos - l
                print(ent, '--rstrip--', text[start_pos:end_pos + 1])

            if category not in ner_labels:
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
        ner_labels,
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
            ner_labels,
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
        i = clean_text(s['uid'])
        guid = str(i)
        text_a = clean_text(s['originalText'])

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

    from theta.modeling import archive_local_model
    archive_local_model(args, submission_file)

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

    poplar_data_file = "./data/poplar_data.json"
    json.dump(poplar_json,
              open(poplar_data_file, 'w'),
              ensure_ascii=False,
              indent=2)
    logger.info(f"Saved {poplar_data_file}")


from theta.modeling import Params, CommonParams, NerParams, NerAppParams, log_global_params

experiment_params = NerAppParams(
    CommonParams(
        dataset_name=dataset_name,
        experiment_name="NER",
        # train_file='E:/dataset/ccks2020_2_task1_train/task1_train.txt',
        # eval_file='E:/dataset/ccks2020_2_task1_train/task1_train.txt',
        # test_file='E:/dataset/ccks2_task1_val/task1_no_val_utf8.txt',
        train_file=Path(dataset_dir, dataset_name, 'train_data.txt'),
        eval_file=Path(dataset_dir, dataset_name, 'train_data.txt'),
        # eval_file='data/task5_dev.txt',
        test_file=Path(dataset_dir, dataset_name, 'test_data.txt'),
        learning_rate=1e-5,
        train_max_seq_length=188,
        eval_max_seq_length=188,
        per_gpu_train_batch_size=32,
        per_gpu_eval_batch_size=32,
        per_gpu_predict_batch_size=32,
        seg_len=186,
        seg_backoff=88,
        num_train_epochs=15,
        fold=9,
        num_augements=2,
        enable_kd=True,
        enable_sda=False,
        sda_teachers=0,
        loss_type="CrossEntropyLoss",  # "FocalLoss",
        model_type="bert",
        model_path=
        "/opt/share/pretrained/pytorch/roberta-wwm-large-ext-chinese",
        # "/opt/share/pretrained/pytorch/bert-base-chinese",
        #  '../../prev_trained_model/bert-wobert-chinese',
        fp16=True,
        best_index="f1",
        seed=6636,
        train_rate=0.9,
        random_type=None),
    NerParams(ner_labels=ner_labels, ner_type='span', no_crf_loss=False))

experiment_params.debug()


def main(args):
    def do_eda(args):
        show_ner_datainfo(ner_labels, train_data_generator, args.train_file,
                          test_data_generator, args.test_file)

    def do_submit(args):
        generate_submission(args)
        ''' 
        from pipeline.ner.utils import theta_submission2poplar
        if not args.data_dir:
            args.data_dir = './' + dataset_dir
        theta_submission2poplar(args)
        '''
        utils_theta_submission.generate_submission_val(args)

    if args.do_eda:
        do_eda(args)

    elif args.do_submit:
        do_submit(args)

    elif args.to_poplar:
        to_poplar(args)

    else:

        # -------------------- Model --------------------
        #  if args.ner_type == 'span':
        #      from theta.modeling.ner_span import NerTrainer
        #  else:
        #      from theta.modeling.ner import NerTrainer

        class AppTrainer(NerTrainer):
            def __init__(self, args, ner_labels):
                super(AppTrainer, self).__init__(args,
                                                 ner_labels,
                                                 build_model=None)

            #  def on_predict_end(self, args, test_dataset):
            #      super(Trainer, self).on_predict_end(args, test_dataset)

        trainer = AppTrainer(args, ner_labels)

        def do_train(args):
            train_examples, val_examples = load_train_val_examples(args)
            trainer.train(args, train_examples, val_examples)

        def do_eval(args):
            args.model_path = args.best_model_path
            _, eval_examples = load_train_val_examples(args)
            model = load_model(args)
            return trainer.evaluate(args, model, eval_examples)

        def do_predict(args):
            args.model_path = args.best_model_path
            test_examples = load_test_examples(args)
            model = load_model(args)
            trainer.predict(args, model, test_examples)
            reviews_file, category_mentions_file = save_ner_preds(
                args, trainer.pred_results, test_examples)
            return reviews_file, category_mentions_file

        if args.do_train:
            do_train(args)

        elif args.do_eval:
            do_eval(args)

        elif args.do_predict:
            do_predict(args)

        elif args.do_experiment:
            '''
            if args.tracking_uri:
                mlflow.set_tracking_uri(args.tracking_uri)
            mlflow.set_exdo_experimentperiment(args.experiment_name)

            with mlflow.start_run(run_name=f"{args.local_id}") as mlrun:
                log_global_params(args, experiment_params)
            '''
            if True:
                # ----- Train -----
                do_train(args)

                # ----- Predict -----
                do_predict(args)

                # ----- Submit -----
                do_submit(args)


if __name__ == '__main__':

    def add_special_args(parser):
        parser.add_argument("--to_poplar", action="store_true")
        return parser

    if experiment_params.ner_params.ner_type == 'span':
        from theta.modeling.ner_span import load_model, get_args, NerTrainer
    else:
        from theta.modeling.ner import load_model, get_args, NerTrainer

    args = get_args(experiment_params=experiment_params,
                    special_args=[add_special_args])
    logger.info(f"args: {args}")

    args.do_eval = True
    main(args)

