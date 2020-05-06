#from nltk.tokenize import ToktokTokenizer
#from newspaper import fulltext
from nltk.tokenize import word_tokenize
from nltk.tokenize import ToktokTokenizer
import sys
import math

# function to clean data based on observed leftover social media text from html
def clean(line):
    line = line.strip().replace("newline_char", " ")
    line = line.replace("NEWLINE_CHAR", "")
    line = line.replace("( opens in new window )", "")
    line = line.replace("click to email this to a friend", "")
    line = line.replace("lick to share on whatsapp", "")
    line = line.replace("click to share on facebook", "")
    line = line.replace("share on facebook", "")
    line = line.replace("click to share on twitter", "")
    line = line.replace("click to share on pinterest", "")
    line = line.replace("click to share on tumblr", "")
    line = line.replace("click to share on google+", "")
    line = line.replace("feel free to share these resources in your social "
                        "media networks , websites and other platforms", "")
    line = line.replace("share share tweet link", "")
    line = line.replace("e-mail article print share", "")
    line = line.replace("read or share this story :", "")
    line = line.replace("share the map view in e-mail by clicking the share "
                        "button and copying the link url .     embed the map "
                        "on your website or blog by getting a snippet of html "
                        "code from the share button .     if you wish to "
                        "provide feedback or comments on the map , or if "
                        "you are aware of map layers or other "
                        "datasets that you would like to see included on our maps , "
                        "please submit them for our evaluation using this this form .", "")
    line = line.replace("share this article share tweet post email", "")
    line = line.replace("skip in skip x embed x share close", "")
    line = line.replace("share tweet pin email", "")
    line = line.replace("share on twitter", "")
    line = line.replace("feel free to weigh-in yourself , via"
                        "the comments section . and while you ’ "
                        "re here , why don ’ t you sign up to "
                        "follow us on twitter us on twitter .", "")
    line = line.replace("follow us on facebook , twitter , instagram and youtube", "")
    line = line.replace("follow us on twitter", "")
    line = line.replace("follow us on facebook", "")
    line = line.replace("play facebook twitter google plus embed", "")
    line = line.replace("play facebook twitter embed", "")
    line = line.replace("enlarge icon pinterest icon close icon", "")
    line = line.replace("follow on twitter", "")
    line = line.replace("autoplay autoplay copy this code to your website or blog", "")
    return line

def clean_data(doc):
    content_cleaned = []
    toktok = ToktokTokenizer()

    for count, file in enumerate(doc.content):
        try:
            text_newspaper = toktok.tokenize(file)
            text_newspaper_cleaned = clean(" ".join(text_newspaper))
            content_cleaned.append(text_newspaper_cleaned.lower())

        except: # pylint: disable=W0702
            print(f"error with {count}")#, file=sys.stderr)
    doc['content_cleaned'] = content_cleaned
    return doc


def truncate(corpus, separator_tag, TOTAL_WORDS):
    result = []
    for count, line in enumerate(corpus):
        line_word_split = line.split()
        if len(line_word_split) < TOTAL_WORDS:
            result.append(line)
        else:
            sources_split = line.split(separator_tag)
            # previous dataset had separator at the end of each example
            if sources_split[-1] == "":
                del sources_split[-1]
            num_sources = len(sources_split)
            words_ar = [source.split() for source in sources_split]
            num_words_ar = [len(words) for words in words_ar]
            per_source_count = math.floor(TOTAL_WORDS / num_sources)
            total_ar = [0] * num_sources
            total = 0
            done = {}
            while total < TOTAL_WORDS and len(done) < len(num_words_ar):
                # e.g. total=499 and still trying to add -- just add from the first doc which isn't done
                if per_source_count == 0:
                    for index, x in enumerate(total_ar):
                        if index not in done:
                            total_ar[index] += TOTAL_WORDS - total
                            break
                    break
                min_amount = min(min([x for x in num_words_ar if x > 0]), per_source_count)
                total_ar = [x + min_amount if index not in done else x for index, x in enumerate(total_ar)]
                for index, val in enumerate(num_words_ar):
                    if val == min_amount:
                        done[index] = True
                num_words_ar = [x - min_amount for x in num_words_ar]
                total = sum(total_ar)
                if len(done) == len(num_words_ar):
                    break
                per_source_count = math.floor((TOTAL_WORDS - total) / (len(num_words_ar) - len(done)))
            final_words_ar = []
            for count_words, words in enumerate(words_ar):
                cur_string = " ".join(words[:total_ar[count_words]])
                final_words_ar.append(cur_string)
            final_str = (" " + separator_tag + " ").join(final_words_ar).strip() # e.g. " story_separator_special_tag "
            result.append(final_str)

    return list(result)


def truncate(df, separator_tag, TOTAL_WORDS):
    result = []
    for count, line in enumerate(df):
        line_word_split = line.split()
        if len(line_word_split) < TOTAL_WORDS:
            result.append(line)
        else:
            sources_split = line.split(separator_tag)
            # previous dataset had separator at the end of each example
            if sources_split[-1] == "":
                del sources_split[-1]
            num_sources = len(sources_split)
            words_ar = [source.split() for source in sources_split]
            num_words_ar = [len(words) for words in words_ar]
            per_source_count = math.floor(TOTAL_WORDS / num_sources)
            total_ar = [0] * num_sources
            total = 0
            done = {}
            while total < TOTAL_WORDS and len(done) < len(num_words_ar):
                # e.g. total=499 and still trying to add -- just add from the first doc which isn't done
                if per_source_count == 0:
                    for index, x in enumerate(total_ar):
                        if index not in done:
                            total_ar[index] += TOTAL_WORDS - total
                            break
                    break
                min_amount = min(min([x for x in num_words_ar if x > 0]), per_source_count)
                total_ar = [x + min_amount if index not in done else x for index, x in enumerate(total_ar)]
                for index, val in enumerate(num_words_ar):
                    if val == min_amount:
                        done[index] = True
                num_words_ar = [x - min_amount for x in num_words_ar]
                total = sum(total_ar)
                if len(done) == len(num_words_ar):
                    break
                per_source_count = math.floor((TOTAL_WORDS - total) / (len(num_words_ar) - len(done)))
            final_words_ar = []
            for count_words, words in enumerate(words_ar):
                cur_string = " ".join(words[:total_ar[count_words]])
                final_words_ar.append(cur_string)
            final_str = (" " + separator_tag + " ").join(final_words_ar).strip() # e.g. " story_separator_special_tag "
            result.append(final_str)

    return list(result)





