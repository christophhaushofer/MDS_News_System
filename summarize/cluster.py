import pandas as pd
import numpy as np
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from utility.utils import *
from utility.clean import *
import time

class LemmaTokenizer:
    # from https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


def calc_sim(df, tokenizer, threshold):
    stopset = stopwords.words('english') + list(string.punctuation) + ["—", '’', '“'] + ["'d", "'ll", "'re", "'s",
                                                                                         "'ve", '``', 'could', 'doe',
                                                                                         'ha', 'might', 'must', "n't",
                                                                                         'need', 'sha', 'wa', 'wo',
                                                                                         'would']

    print('------ calcualting the TF IDF Matrix')
    # calculate TF IDF / cosim https://stackoverflow.com/questions/8897593/how-to-compute-the-similarity-between-two-text-documents/14831884#14831884
    v = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words=stopset, tokenizer=tokenizer)
    tfidf = v.fit_transform(df.content_cleaned)
    pairwise_similarity = tfidf * tfidf.T

    # prepare sparse matrix
    arr = pairwise_similarity.toarray()
    print("--- %s seconds ---" % (time.process_time()))
    print(f'------- TF IDF Matrix calculated with dim: {pairwise_similarity.shape}')

    '''
    Cluster Objects by similarity (tf idf value)
    :return: Pandas Dataframe which contains Clusternames and objects of Cluster
    '''

    # prerequisites
    cluster_list = []
    s = []
    cluster = 0

    # read existing clusters and get it to list
    existing_clusters = get_clusters()
    existing_clusters['sim_article_id'].replace(to_replace="[{}]", value="", regex=True, inplace=True)
    existing_clusters = list(existing_clusters['sim_article_id'])

    print("--- %s seconds ---" % (time.process_time()))
    print('------ Clustering')
    for ref_doc_id, row in df.iterrows():

        # select tf_idf values above threshold and below 0.99 to avoid too similar articles
        doc_id = np.where(np.logical_and(arr[ref_doc_id] > threshold, arr[ref_doc_id] < 0.99))[0]

        if doc_id.tolist():

            # get values of similar articles
            sim_article_value = arr[ref_doc_id][doc_id]

            # get indices of similar articles (including Reference document)
            sim_article_ids = [ref_doc_id] + doc_id.tolist()
            sim_article_values = [1.0] + sim_article_value.tolist()

            # get metadata for cluster documents
            authors = [x for x in df.iloc[sim_article_ids].author]
            sources = [x for x in df.iloc[sim_article_ids].source]
            word_counts = [x for x in df.iloc[sim_article_ids].wordCount]
            dates = [x.strftime("%d-%b-%Y (%H:%M:%S)") for x in df.iloc[sim_article_ids].pubDate]
            input = ' story_separator_special_tag '.join([x for x in df.iloc[sim_article_ids].content_cleaned])

            # var to check if cluster already in list
            lookup_ids = sim_article_ids.copy()
            lookup_ids.sort()

            if lookup_ids not in s and lookup_ids not in existing_clusters:
                cluster_list.append(
                    {'cluster': cluster, 'sim_article_id': sim_article_ids, 'sim_article_values': sim_article_values,
                     'authors': authors, 'sources': sources, 'dates': dates, 'wordCounts': word_counts, 'input_articles': input})
                s.append(lookup_ids)
                cluster += 1
            else:
                next
    # delete tfidf array
    del arr
    print(f'Found {len(cluster_list)} Clusters in {df.shape[0]} Articles!')
    print("--- %s seconds ---" % (time.process_time()))
    pd.DataFrame(cluster_list).to_csv('output/clusters.txt', header=True)
    return cluster_list

def make_input_data(df, cluster_list, story_separator):
    input_data = []
    for cluster in cluster_list:
        d = []
        for ids in cluster['sim_article_id']:
            d.append(df.iloc[ids].content_cleaned)
        input_data.append(story_separator.join(d))

    with open('data\input_data.txt', 'w', encoding="utf-8") as fw:
        for sample in input_data:
            fw.write(sample + "\n")


