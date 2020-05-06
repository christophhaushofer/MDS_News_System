import time
from lexrank import LexRank
from lexrank.mappings.stopwords import STOPWORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.summarization.textcleaner import split_sentences
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import math

class LemmaTokenizer:
    # from https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

def lexrank_summarize(corpus, story_separator_special_tag):
    list_of_summarization = []

    documents = [split_sentences(sample.replace(story_separator_special_tag, "\n")) for sample in corpus]
    print("[" + "Document Size: " + str(len(documents)) + "]")
    print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", "Begin building LexRank model...")
    #
    lxr = LexRank(documents, stopwords=STOPWORDS['en'])
    print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", "LexRank model successfully built...")

    for i in range(len(documents)):
        sample = documents[i]
        summary = lxr.get_summary(sample, summary_size=len(sample))
        articles = corpus[i].split(story_separator_special_tag)

        words_counter = 0
        summary_counter = 0
        tmp_summary = [[] for _ in range(len(articles))]

        while words_counter < 500 and summary_counter < len(summary):
            flag = 0
            for j in range(len(articles)):
                if summary[summary_counter] in articles[j]:
                    tmp_summary[j].append(summary[summary_counter])
                    words_counter += len(summary[summary_counter].split(" "))
                    flag = 1
            if flag == 0:
                print("[Error] Summary not in original sample.", summary[summary_counter], i)
            summary_counter += 1

        # print("words_counter, summary_counter, total summary", words_counter, summary_counter, len(summary))
        for k in range(len(tmp_summary)):
            tmp_summary[k] = " newline_char ".join(tmp_summary[k])
        list_of_summarization.append(" story_separator_special_tag ".join(tmp_summary))

        if i % 100 == 0:
            print("------")
            print(i)
            print("------")
    # if i == 100:
    # 	break

    return list_of_summarization


def lexrank_summarize_simple(corpus, story_separator_special_tag):
    list_of_summarization = []

    documents = [split_sentences(sample.replace(story_separator_special_tag, "\n")) for sample in corpus]
    print("[" + "Document Size: " + str(len(documents)) + "]")
    print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", "Begin building LexRank model...")
    #
    lxr = LexRank(documents, stopwords=STOPWORDS['en'])
    print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", "LexRank model successfully built...")

    for i in range(len(documents)):
        sample = documents[i]
        summary = lxr.get_summary(sample, summary_size=math.ceil(round(len(sample) * 0.2)))

        v = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words=STOPWORDS['en'], tokenizer=LemmaTokenizer())
        tfidf = v.fit_transform(summary)
        pairwise_similarity = tfidf * tfidf.T

        d = []
        for index, value in enumerate(summary):
            tf = pairwise_similarity[index].toarray()
            if tf[0, index - 1] < 0.5:
                d.append(value)

            tmp_summary = ' '.join(d)
        list_of_summarization.append(tmp_summary)

        if i % 100 == 0:
            print("------")
            print(i)
            print("------")

    return list_of_summarization


def lexrank_summarize_simple(corpus, story_separator_special_tag):
    list_of_summarization = []

    documents = [split_sentences(sample.replace(story_separator_special_tag, "\n")) for sample in corpus]
    print("[" + "Document Size: " + str(len(documents)) + "]")
    print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", "Begin building LexRank model...")
    #
    lxr = LexRank(documents, stopwords=STOPWORDS['en'])
    print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", "LexRank model successfully built...")

    for i in range(len(documents)):
        sample = documents[i]
        summary = lxr.get_summary(sample, summary_size=math.ceil(round(len(sample) / 2)))

        v = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words=STOPWORDS['en'], tokenizer=LemmaTokenizer())
        tfidf = v.fit_transform(summary)
        pairwise_similarity = tfidf * tfidf.T

        d = []
        for index, value in enumerate(summary):
            tf = pairwise_similarity[index].toarray()
            if tf[0, index - 1] < 0.5:
                d.append(value)

            tmp_summary = ' '.join(d)
        list_of_summarization.append(tmp_summary)

        if i % 100 == 0:
            print("------")
            print(i)
            print("------")

    return list_of_summarization