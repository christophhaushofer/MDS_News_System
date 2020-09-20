import pandas as pd
import numpy as np
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from scraper.models import *
from summarizer.utilities import DocLoader

class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, data):
        return [self.wnl.lemmatize(t) for t in word_tokenize(data)]

class DocCluster:
    def __init__(self):

        self.engine = db_connect()
        self.threshold = 0.4
        self.cluster = 0

    def calc_sim(self, data):
        stopset = stopwords.words('english')
        stopset = stopset + list(string.punctuation)
        stopset = stopset + ["—", '’', '“'] + ["'d", "'ll", "'re", "'s", "'ve", '``', 'could', 'doe', 'ha',
                                               'might', 'must',
                                               "n't", 'need', 'sha', 'wa', 'wo', 'would']
        self.data = data
        v = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words=stopset, tokenizer=LemmaTokenizer())
        tfidf = v.fit_transform(self.data.content)
        sim_matrix = cosine_similarity(tfidf)
        return sim_matrix

    def _check_existing_clusters(self, tablename):
        check = self.engine.has_table(tablename)
        if check:
            data = pd.read_sql_query(f'select * from {tablename}', con=self.engine)
            data = data.sort_values(by=['sim_article_id'])
            self.existing_clusters = data.groupby('cluster')['sim_article_id'].apply(list)
            self.cluster = max(self.existing_clusters.index) + 1
        else:
            self.existing_clusters = pd.DataFrame()
            self.cluster = 0

    def make_cluster(self, data, sim_matrix, tablename, threshold):
        self.sim_matrix = sim_matrix
        self.data = data
        self.threshold = threshold
        data_dim = range(data.shape[0])
        cluster_list = []
        input_list = []
        lookup = []
        self._check_existing_clusters(tablename)
        for i in data_dim:
            # select tf_idf values above threshold and below 0.99 to avoid too similar articles
            data_id = np.where(np.logical_and(self.sim_matrix[i] > self.threshold, self.sim_matrix[i] < 0.99))[0]
            if data_id.tolist():
                # get indices of similar articles (including Reference dataument)
                sim_article_ids = [self.data.index[i]] + self.data.index[data_id].tolist()
                # sort ids by pubDate
                sim_article_ids = self.data.pubDate.loc[sim_article_ids].sort_values(ascending=False).index.tolist()
                # var to check if cluster already in list
                lookup_ids = sim_article_ids.copy()
                not_duplicate = lookup_ids not in lookup
                not_in_db = lookup_ids not in list(self.existing_clusters)
                if not_duplicate and not_in_db:
                    for sim_article_id in sim_article_ids:
                        author = self.data.loc[sim_article_id].author
                        source = self.data.loc[sim_article_id].source
                        link = self.data.loc[sim_article_id].link
                        pubDate = self.data.loc[sim_article_id].pubDate.strftime("%d-%b-%Y (%H:%M:%S)")
                        cluster_list.append({'cluster': self.cluster,
                             'sim_article_id': sim_article_id,
                             'author': author,
                             'link': link,
                             'source': source,
                             'date': pubDate})
                    # make input data
                    self.input_data_trunc = ' story_separator_special_tag '.join(
                        [x for x in self.data.loc[sim_article_ids].content_cleaned])
                    input_list.append(
                    {'cluster': self.cluster,
                     'input_data': self.input_data_trunc})
                    lookup.append(lookup_ids)
                    self.cluster += 1
                else:
                    next

        cluster_data = pd.DataFrame(cluster_list)
        docl = DocLoader()
        docl._write_to_db(cluster_data, tablename, 'append')

        input_data = pd.DataFrame(input_list)
        docl._write_to_db(input_data, 'input_data', 'replace')
        docl._write_to_txt(input_data, 'data', 'input_data')
        print('Data clustered and stored in database')