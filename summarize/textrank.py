from gensim.summarization.summarizer import summarize
from gensim.summarization.textcleaner import split_sentences
import os

def textrank_summarize(corpus, story_separator_special_tag):
    print("Begin summarizing...")

    list_of_summarization = []

    error_counter = 0
    null_summarization_counter = 0
    for i in range(len(corpus)):
        sample = corpus[i].strip()
        articles = sample.split(story_separator_special_tag)

        try:
            summarization = summarize("\n".join(articles), word_count=500, split=True)
            if len(summarization) == 0:
                null_summarization_counter += 1
                summarization = split_sentences("\n".join(articles))
                if len(summarization) == 0:
                    print("*** No Summarization ***", i)
        except ValueError:
            print("ValueError, sample", sample)
            summarization = sample
            list_of_summarization.append(summarization)
            error_counter += 1
            continue

        tmp_list_of_summarization = [[] for _ in range(len(articles))]
        for sent in summarization:
            flag = 0
            for j in range(len(articles)):
                if sent in articles[j]:
                    tmp_list_of_summarization[j].append(sent)
                    flag = 1
            if flag == 0:
                print(i, "****", sent, (sent in " ".join(articles)))

        for k in range(len(tmp_list_of_summarization)):
            tmp_list_of_summarization[k] = " newline_char ".join(tmp_list_of_summarization[k])

        list_of_summarization.append(story_separator_special_tag.join(tmp_list_of_summarization))

        if i % 100 == 0:
            print(i)
            print("------")
    # if i == 5000:
    # 	break

    return list_of_summarization #, error_counter, null_summarization_counter

