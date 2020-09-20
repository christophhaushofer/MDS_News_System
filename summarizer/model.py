import os
from scraper.models import *
import pandas as pd
from summarizer.utilities import DocLoader
import csv

class HimapModel:
    def __init__(self, input_file, output_table):
        self.input_file = input_file
        self.out = pd.DataFrame()

        # define parameters for Hi-MAP Model
        self.batch_size = 1
        self.beam_size = 8
        self.max_length = 300
        self.min_length = 200
        self.beta = 5
        self.alpha = 0.9
        self.widow_size = 0.02

        filePath = 'output/output_scored.txt'
        if os.path.exists(filePath):
            os.remove(filePath)

        opt = f'python translate.py -gpu 0 \
            			-batch_size {self.batch_size} \
            			-beam_size {self.beam_size} \
            			-model pretrained_models/newser_mmr/Feb17__step_20000.pt \
            			-src data/{input_file}.txt  \
                        -output output/output.txt \
            			-min_length {self.min_length} \
            			-max_length {self.max_length} \
            			-verbose \
            			-stepwise_penalty \
            			-coverage_penalty summary \
            			-beta {self.beta} \
            			-length_penalty wu \
            			-alpha {self.alpha} \
                        -verbose \
            			-block_ngram_repeat 3 \
            			-ignore_when_blocking "story_separator_special_tag"'
        os.system(opt)

        with open('output\output_scored.txt', 'r', encoding="utf-8") as f:
            for row in csv.reader(f, delimiter='\t'):
                self.out = self.out.append(pd.DataFrame({'score': float(row[0].strip()), 'sum': row[1].strip()}, index=[0]),
                                 ignore_index=True)

        self.data = self.out
        DocLoader()._write_to_db(self.data, output_table, 'append')