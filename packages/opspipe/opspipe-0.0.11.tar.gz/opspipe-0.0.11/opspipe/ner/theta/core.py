# -*- coding: utf-8 -*-
from tqdm import tqdm
from loguru import logger
from theta.utils import load_json_file  
from theta.modeling.ner_utils import InputExample  
from theta.utils import seg_generator 
from theta.modeling import load_ner_examples,get_ner_preds_reviews 

def do_predict(args,trainer,model,txt):
    test_examples = load_test_one(args,txt)
    trainer.predict(args, model, test_examples)
    reviews, _ = get_ner_preds_reviews(trainer.pred_results, test_examples, args.seg_len, args.seg_backoff)
    return reviews

def trainer_model(experiment_params,ner_labels):
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
    
    return trainer,model,args
    
# -------------------- Data -------------------- 
def test_data_generator(test_file):
    lines = load_json_file(test_file)
    for i, s in enumerate(tqdm(lines)): 
        guid = str(i)
        try:
            guid =  s['guid']
        except :
            None
             
        text_a = s['originalText']

        yield guid, text_a, None, None


def load_test_examples(args):
    test_base_examples = load_ner_examples(test_data_generator,
                                           args.test_file,
                                           seg_len=args.seg_len,
                                           seg_backoff=args.seg_backoff)

    logger.info(f"Loaded {len(test_base_examples)} test examples.")
    return test_base_examples 

def load_test_one(args,text_a): 
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