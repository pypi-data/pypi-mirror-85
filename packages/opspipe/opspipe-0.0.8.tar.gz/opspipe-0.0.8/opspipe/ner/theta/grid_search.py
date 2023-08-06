# -*- coding: utf-8 -*-
'''
'''

import os, sys, json, random, copy
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import os, sys
from tqdm import tqdm
from loguru import logger
from theta.utils import load_json_file, split_train_eval_examples
from theta.modeling import LabeledText, load_ner_examples, load_ner_labeled_examples, save_ner_preds, show_ner_datainfo
from pathlib import Path
from pipeline.ner.theta import do_predict, trainer_model
from theta.modeling import Params, CommonParams, NerParams, NerAppParams, log_global_params

#  if os.environ['NER_TYPE'] == 'span':
#      from theta.modeling.ner_span import load_model, get_args
#  else:
#      from theta.modeling.ner import load_model, get_args


import os
import numpy as np

best_model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outputs', 'latest', 'best')
base_model_path = '/opt/share/pretrained/pytorch/bert-base-chinese'

# read_txts(Path(dataset_dir,dataset_name,'labels.txt'))
ner_labels = [
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
    text = str(text).replace('\n', ' ')
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


class thetaNER():
    def __init__(self, dataset_name='ccf2020_business_ner', dataset_dir='datasets',
                 num_train_epochs=1,
                 train_max_seq_length=258,
                 seg_len=256,
                 seg_backoff=128, train_rate=0.9,
                 learning_rate=2e-5,
                 batch_size=4,
                 fold=0
                 ):

        self.num_train_epochs = num_train_epochs
        self.train_max_seq_length = train_max_seq_length
        self.seg_len = seg_len
        self.seg_backoff = seg_backoff
        self.dataset_dir = dataset_dir
        self.dataset_name = dataset_name
        self.train_rate = train_rate

        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.fold = fold
        self.model_path = base_model_path


    # print(self.get_params())
    def fit(self, parm):
       print('aaaa')

    def predict(self, X_new):
        return [],[]

    def get_params(self, deep=True):
        """Get parameters for this estimator.

        Parameters
        ----------
        deep : boolean, optional
            If True, will return the parameters for this estimator and
            contained subobjects that are estimators.

        Returns
        -------
        params : mapping of string to any
            Parameter names mapped to their values.
        """
        out = dict()
        for key in ['learning_rate', 'batch_size', 'fold']:  # 这里是所用超参数的list
            value = getattr(self, key, None)
            if deep and hasattr(value, 'get_params'):
                deep_items = value.get_params().items()
                out.update((key + '__' + k, val) for k, val in deep_items)
            out[key] = value
        return out

    def set_params(self, **params):
        """Set the parameters of this estimator.

        The method works on simple estimators as well as on nested objects
        (such as pipelines). The latter have parameters of the form
        ``<component>__<parameter>`` so that it's possible to update each
        component of a nested object.

        Returns
        -------
        self
        """
        if not params:
            # Simple optimization to gain speed (inspect is slow)
            return self
        valid_params = self.get_params(deep=True)

        for key, value in params.items():
            if key not in valid_params:
                raise ValueError('Invalid parameter %s for estimator %s. '
                                 'Check the list of available parameters '
                                 'with `estimator.get_params().keys()`.' %
                                 (key, self))
            setattr(self, key, value)
            valid_params[key] = value

        return self

    def score(self, X, y=None, sample_weight=None):


        return 111  # myloss_fun(y, self.predict(X), sample_weight=sample_weight)



if __name__ == '__main__':
    from sklearn.model_selection import RandomizedSearchCV

    param_grid = [
        {
         'fold':[1]
         },
    ]

    thetaNER = thetaNER()
    grid_search = RandomizedSearchCV(thetaNER, param_grid)
    grid_search.fit(np.arange(0,5))

    #返回最优的训练器
    print("Test set score:{:.2f}".format(grid_search.score(X=None)))
    print("Best parameters:{}".format(grid_search.best_params_))
    print("Best score on train set:{:.2f}".format(grid_search.best_score_))
