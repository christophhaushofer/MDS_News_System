from scraper.pipelines import *
from scraper.spiders import *
from summarizer.cluster import DocCluster
from summarizer.clean import DocClean
from summarizer.utilities import DocLoader
from summarizer.model import HimapModel
from scrapy.crawler import CrawlerProcess

def settings_scrapy():
    global settings
    settings = dict()
    settings['USER_AGENT'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    settings['ITEM_PIPELINES'] = dict()
    settings['ITEM_PIPELINES']['scraper.pipelines.DbPipeline'] = 801



if __name__ == "__main__":
    ## Data extraction
    # start crawling
    settings_scrapy()

    process = CrawlerProcess(settings=settings)
    process.crawl(ApressSpider)
    process.crawl(PoliticoSpider)
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
    nDays = 1

    dl = DocLoader()
    data = dl.select_data("news_data", nDays)

    ## NLP Pipeline
    # Clean and tokenize
    total_words = 500
    clean = DocClean()
    data = clean.clean_data(data, total_words)

    # Calculate Similarity of Articles via Cosine similarity
    cl = DocCluster()
    s_m = cl.calc_sim(data)

    # Make Clusters
    cl.make_cluster(data, s_m, 'cluster_data', 0.4)

    ## Model
    # Start HIMAP model
    HimapModel('input_data', 'article_summaries')