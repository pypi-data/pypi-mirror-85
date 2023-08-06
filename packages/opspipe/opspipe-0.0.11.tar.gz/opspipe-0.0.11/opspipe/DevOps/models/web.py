#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import os, sys, json, random, copy
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
from tqdm import tqdm
from loguru import logger
from theta.utils import load_json_file, split_train_eval_examples
from theta.modeling import LabeledText, load_ner_examples, load_ner_labeled_examples, save_ner_preds, show_ner_datainfo
from pathlib import Path
from theta.modeling.ner_utils import InputExample
from pipeline import lump_logs
from theta.utils import seg_generator
from pipeline.utils import read_txts 
from theta.modeling import load_ner_examples, save_ner_preds,get_ner_preds_reviews
from theta.modeling import Params, CommonParams, NerParams, NerAppParams, log_global_params
from starlette.responses import RedirectResponse
import uvicorn
from fastapi import FastAPI
app = FastAPI()


#  if os.environ['NER_TYPE'] == 'span':
#      from theta.modeling.ner_span import load_model, get_args
#  else:
#      from theta.modeling.ner import load_model, get_args

dataset_dir = 'datasets'
dataset_name = 'ner_bid_notice'
# TODO 优化 read_txts
ner_labels = read_txts(Path(dataset_dir,'labels.txt'))
ner_labels = [la.replace('\n','') for la in ner_labels]

# -------------------- Data --------------------

def clean_text(text):
    text = str(text).replace('\n',' ')
    # if text:
    #    text = text.strip()
    # text = re.sub('\n', ' ', text)
    return text

def test_data_generator(test_file):
    lines = load_json_file(test_file)
    for i, s in enumerate(tqdm(lines)):
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

model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'outputs','latest','best')
print(model_path)
def init_theta(): 
    global args
    global trainer
    global model 
    experiment_params = NerAppParams(
        CommonParams(
            dataset_name=dataset_name,
            experiment_name="NER", 
            train_max_seq_length=258,
            eval_max_seq_length=258,
            per_gpu_train_batch_size=8,
            per_gpu_eval_batch_size=8,
            per_gpu_predict_batch_size=8,
            seg_len=256,
            seg_backoff=128,  
            model_type="bert",
            model_path=model_path,
            fp16=True,   
            random_type=None),
        NerParams(ner_labels=ner_labels, ner_type='span', no_crf_loss=False))
    
    experiment_params.debug()
    
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
    
    class AppTrainer(NerTrainer):
        def __init__(self, args, ner_labels):
            super(AppTrainer, self).__init__(args, ner_labels, build_model=None)
    
    trainer = AppTrainer(args, ner_labels)
    
    #args.model_path = args.best_model_path
    model = load_model(args) 

init_theta()

def do_predict(args,txt):
    test_examples = load_test_one(args,txt)
    trainer.predict(args, model, test_examples)
    reviews, _ = get_ner_preds_reviews(trainer.pred_results, test_examples, args.seg_len, args.seg_backoff)
    return reviews

long_labels = []
@app.get("/predict/{text}")
async def read_item(text: str):
    #text = '中国人民共和国' #treat_text(text)
    #TODO 转换为 文本
    lump_logs('base64数据',text)
    reviews = do_predict(args,text)
    
    final_result = gen_submit_file(reviews, long_labels=long_labels)
    output_string = json.dumps({'result': final_result}, ensure_ascii=False)
    lump_logs('返回json',output_string)
    return output_string
 

def gen_submit_file(reviews, long_labels):
    #precit_data_json = read_json_data(predict_result_file)
    final_result = []
    index = 0
    for key in reviews:
        # 获取原始id
        index += 1
        result = reviews[key]
        entities = result['entities']
        src_text = result['text']

        long_labels_result_dict = {}
        for label in long_labels:
            r = LongLabelResult(label, -1, -1)
            long_labels_result_dict[label] = r

        for cur in entities:
            category = cur['category']
            start = cur['start']
            end = cur['end']
            label_val = cur['mention']

            if category.endswith('_开始') or category.endswith('_结束'):
                # 记录位置
                tag = category[len(category) - 2:]
                cur_long_label = category[0: len(category) - 3]
                r = long_labels_result_dict[cur_long_label]
                if tag == "开始":
                    r.start = start
                else:
                    r.end = end

            else:
                final_result.append({
                    'categoryId': category,
                    'name': label_val,
                    'startIndex': start,
                    'endIndex': end
                })

        for key in long_labels_result_dict:
            r = long_labels_result_dict[key]
            if r.start > -1 and r.end > -1:
                final_result.append({
                    'categoryId': r.text,
                    'name': src_text[r.start:r.end + 1],
                    'startIndex': r.start,
                    'endIndex': r.end
                })

    return final_result

class LongLabelResult(object):
    """
    常文本预测结果
    """
    def __init__(self, text, start, end):
        self.text = text
        self.start = start
        self.end = end

def treat_text(text):
    '''
    import re
    text_drop = re.sub('　', '', text)
    text_drop = re.sub('\t', '', text_drop)
    text_drop = text_drop.replace("\r", "")
    text_drop = text_drop.replace("\n", "。")
    text_drop = text_drop.replace("�", "")
    pattern = r"[\s?]"
    text_drop = re.sub(pattern, "", text_drop)
    text_drop = text_drop.replace("。。", "。")
    text_drop = text_drop.replace("。。", "。")
    text_drop = text_drop.replace("。。", "。")
    '''
    return text


def load_test_one(args,text_a):
    # TOTO 迁移至pipeline
    examples = []
    for (seg_text_a, ), text_offset in seg_generator((text_a, ), args.seg_len,
                                                     args.seg_backoff):
        examples.append(
            InputExample(guid=str(1),
                         text_a=seg_text_a,
                         labels='',
                         text_offset=text_offset))
    logger.info(f"Loaded {len(examples)} examples.")

    return examples
 
@app.get("/")
async def root():
    return RedirectResponse('/docs')

if __name__ == '__main__': 
    #init_theta() 
    #args.do_predict = True 
    #do_predict(args,'染个发达萨罗就发生的发')
    uvicorn.run(app='web:app', host="127.0.0.1", port=8003, reload=True, debug=True)