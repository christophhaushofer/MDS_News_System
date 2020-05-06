import os
#from dotenv import load_dotenv
from os.path import join, dirname
#from sqlalchemy.engine.url import URL
#from sqlalchemy import create_engine
#from utility.clean import *
import pandas as pd
#import numpy as np
#import string
#from sklearn.feature_extraction.text import TfidfVectorizer
#from nltk.corpus import stopwords
#from nltk.stem import WordNetLemmatizer
#from nltk.tokenize import word_tokenize
from scrapy.crawler import CrawlerProcess
#from sqlalchemy.orm import sessionmaker
from scraper.models import *
from scraper.spiders import *
from scrapy.exceptions import DropItem
from datetime import datetime as dt
from datetime import timedelta
from utility.utils import *
import time
from summarize.cluster import *
from utility.clean import *
import pandas as pd


def write_output():
    global json
    d = dict()
    d_out = {}
    with open("output/out_eval/pred.txt", encoding='utf-8') as f:
        row_nr = 0
        for line in f:
            row_nr += 1
            d_out[f"PRED_{row_nr}"] = line.split(": –")[1].strip()
    d_score = {}
    with open("output/out_eval/score.txt", encoding='utf-8') as f:
        row_nr = 0
        for line in f:
            row_nr += 1
            d_score[f"SCORE_{row_nr}"] = line.split(": ")[1].strip()
    d['output'] = d_out
    d['score'] = d_score
    output = dict()
    output.update(d)
    # delete score, pred file
    os.remove("output/out_eval/score.txt")
    os.remove("output/out_eval/pred.txt")
    import json
    json = json.dumps(output)
    f = open("output/outputEval.txt", "w", encoding='utf-8')
    f.write(json)
    f.close()

def write_output_txt():
    global json
    d = pd.DataFrame()
    d_out = []
    with open("output/out_eval/pred.txt", encoding='utf-8') as f:
        row_nr = 0
        for line in f:
            row_nr += 1
            d_out.append(line.split(": –")[1].strip())
    d_score = []
    with open("output/out_eval/score.txt", encoding='utf-8') as f:
        row_nr = 0
        for line in f:
            row_nr += 1
            d_score.append(line.split(": ")[1].strip())
    d['output'] = d_out
    d['score'] = d_score

    # delete score, pred file
    os.remove("output/out_eval/score.txt")
    os.remove("output/out_eval/pred.txt")

    d.to_csv("output/outputEval.txt", header=True)

if __name__ == "__main__":
    # start crawling
    settings = dict()
    settings['USER_AGENT'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    settings['ITEM_PIPELINES'] = dict()
    settings['ITEM_PIPELINES']['__main__.DuplicatesPipeline'] = 801
    settings['ITEM_PIPELINES']['__main__.DbPipeline'] = 801

    process = CrawlerProcess(settings=settings)
    process.crawl(ApressSpider)
    process.crawl(PoliticoSpider)
    process.crawl(AljazeeraSpider)
    process.crawl(BbcSpider)
    process.crawl(CbnSpider)
    process.crawl(CnnSpider)
    process.crawl(France24Spider)
    process.crawl(LatimesSpider)
    process.crawl(NytimesSpider)
    process.crawl(ObserverSpider)
    process.crawl(ReutersSpider)
    process.crawl(TelegraphSpider)
    process.crawl(TheguardianSpider)
    process.crawl(ThetimesSpider)
    process.crawl(ThetimesUKSpider)
    process.crawl(TimesofindiaSpider)
    process.crawl(ViceSpider)
    process.crawl(WiredSpider)
    process.start()

    # Loading Data from DB
    print('----- Load data')
    articles = get_data("newsdata")
    print("--- %s seconds ---" % (time.process_time()))

    # filter out articles of last X days. Here is a workaround
    #n_days = 7
    #data = articles.loc[articles.pubDate >= (dt.now().astimezone()- timedelta(days=n_days))]
    data = articles

    # prepare data
    print('----- Data cleaning')
    data = clean_data(data)
    print("--- %s seconds ---" % (time.process_time()))

    # Calculate Similarity of Articles via CosinDistance
    print('----- Calculate similarity of Articles')
    clusters = calc_sim(data, LemmaTokenizer(), 0.5)
    print("--- %s seconds ---" % (time.process_time()))

    # truncate input
    print('----- Truncate data')
    data.content_cleaned = truncate(data.content_cleaned, ' story_separator_special_tag ', 500)
    print("--- %s seconds ---" % (time.process_time()))

    # organize data by clusters and prepare them to be read by summarizer
    print('----- Make input file')
    make_input_data(data, clusters, ' story_separator_special_tag ')
    print("--- %s seconds ---" % (time.process_time()))

    # start HIMAP model
    # outputfile
    output_file = f"output_HIMAP_{dt.now().astimezone().year}-{dt.now().astimezone().day}-{dt.now().astimezone().month}-{dt.now().astimezone().hour}-{dt.now().astimezone().minute}.txt"
    
    # define parameters for Hi-MAP Model
    batch_size = 2
    beam_size = 1
    max_length = 300
    min_length = 50
    beta = 5
    alpha = 0.9
    widow_size = 0.02

    # -beam_size {beam_size} \ rausgenommen zum testen
    opt = f'python translate.py -gpu 0 \
			-batch_size {batch_size} \
            -beam_size {beam_size} \
			-model pretrained_models/newser_mmr/Feb17__step_20000.pt \
			-src data/input_data.txt  \
            -output output/{output_file} \
			-min_length {min_length} \
			-max_length {max_length} \
			-verbose \
			-stepwise_penalty \
			-coverage_penalty summary \
			-beta {beta} \
			-length_penalty wu \
			-alpha {alpha} \
			-verbose \
			-block_ngram_repeat 3 \
			-ignore_when_blocking "story_separator_special_tag"  \
			-window_size={widow_size} \
			-report_bleu \
            -replace_unk'
    os.system(opt)

    # write output in dict

    write_output_txt()

    print("--- %s seconds ---" % (time.process_time()))

