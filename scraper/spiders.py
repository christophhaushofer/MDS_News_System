import scrapy
from scrapy.loader import ItemLoader
import hashlib
from scraper.items import NewsArticle


class ApressSpider(scrapy.Spider):
    name = 'apress'

    start_urls = [
        "http://www.apnews.com/apf-topnews",
        "https://apnews.com/apf-intlnews",
        "https://apnews.com/apf-politics",

    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath('//a[contains(@class, "Component-headline")]/@href').extract():
            request = scrapy.Request(response.urljoin(item), callback=self.parse_page)
            yield request

    def parse_page(self, response):

        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            title = response.xpath('//meta[contains(@property, "og:title")]//@content').extract_first()
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//meta[contains(@property, "og:title")]//@content')
            l.add_value('file_id', file_id)
            l.add_xpath('title', '//meta[contains(@property, "og:title")]//@content')
            l.add_value('link', response.url)
            l.add_xpath('description', '//meta[contains(@name, "description")]//@content')
            l.add_xpath('author', '//span[contains(@class, "Component-bylines")]//text()')
            l.add_xpath('content', '//div[contains(@class, "Article")]//p//text()')
            l.add_xpath('pubDate', '//meta[contains(@property, "article:published_time")]//@content')
            l.add_value('source', 'apress')

            yield l.load_item()
        else:
            next

class PoliticoSpider(scrapy.Spider):
    name = 'politico'

    start_urls = [
        "http://www.politico.com/rss/congress.xml",
        "http://www.politico.com/rss/healthcare.xml",
        "http://www.politico.com/rss/defense.xml",
        "http://www.politico.com/rss/economy.xml",
        "http://www.politico.com/rss/energy.xml",
        "http://www.politico.com/rss/politics08.xml"
    ]

    def parse(self, response):
        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath("//channel/item"):

           request = scrapy.Request(item.xpath('link//text()').extract_first(),
                                 callback=self.parse_page)
           request.cb_kwargs['title'] = item.xpath('title//text()').extract_first()
           request.cb_kwargs['description'] = item.xpath('(desc|description)//text()').extract_first()
           request.cb_kwargs['pubDate'] = item.xpath('(date|pubDate)//text()').extract_first()
           request.cb_kwargs['author'] = item.xpath('(author|creator)//text()').extract_first()
           yield request

    def parse_page(self, response, title, description, pubDate, author):
        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//*//h2[contains(@class, "headline")]//text()')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_value('description',description)
            l.add_value('author', author)
            l.add_xpath('content', '//div[contains(@class, "story-text")]//p//text()')
            l.add_value('pubDate', pubDate)
            l.add_value('source', 'politico')

            yield l.load_item()
        else:
            next

class AljazeeraSpider(scrapy.Spider):
    name = 'aljazeera'

    start_urls = [
        "http://www.aljazeera.com/xml/rss/all.xml"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath("//channel/item"):

           request = scrapy.Request(item.xpath('link//text()').extract_first(),
                                 callback=self.parse_page)
           request.cb_kwargs['title'] = item.xpath('title//text()').extract_first()
           request.cb_kwargs['description'] = item.xpath('(desc|description)//text()').extract_first()
           request.cb_kwargs['pubDate'] = item.xpath('(date|pubDate)//text()').extract_first()
           #request.cb_kwargs['author'] = item.xpath('(author|creator)//text()').extract_first()
           yield request

    def parse_page(self, response, title, description, pubDate):

        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'news':

            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//*//h1[contains(@class, "post-title") or contains(@class, "heading-story")]//text()')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_value('description',description)
            l.add_value('author', 'Al Jazeera')
            l.add_xpath('content', '//div[contains(@class,"article-p-wrapper") or'
                                    'contains(@class,"article-body")]//p//text()')
            l.add_xpath('content', '//div[contains(@class,"article-p-wrapper") or'
                                    'contains(@class,"article-body")]//h2//text()')
            l.add_value('pubDate', pubDate)
            l.add_xpath('source', '//*//div[@class="article-body-artSource"]/p//text()')

            yield l.load_item()
        else:
            next

class BbcSpider(scrapy.Spider):
    name = 'bbc'

    start_urls = [
        "http://feeds.bbci.co.uk/news/world/rss.xml"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath("//channel/item"):

           request = scrapy.Request(item.xpath('link//text()').extract_first(),
                                 callback=self.parse_page)
           request.cb_kwargs['title'] = item.xpath('title//text()').extract_first()
           request.cb_kwargs['description'] = item.xpath('(desc|description)//text()').extract_first()
           request.cb_kwargs['pubDate'] = item.xpath('(date|pubDate)//text()').extract_first()
           request.cb_kwargs['author'] = item.xpath('(author|creator)//text()').extract_first()
           yield request

    def parse_page(self, response, title, description, pubDate, author):

        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//meta[contains(@property, "og:title")]//@content')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_value('description', description)
            l.add_xpath('author', '//meta[contains(@property, "article:author")]//@content')
            l.add_xpath('content', '//div[contains(@class, "story-body__inner") or'
                                    'contains(@id, "story-body") or'
                                    'contains(@class, "media__summary")]//p//text()')
            l.add_xpath('content', '//div[contains(@class, "story-body__inner")]//h2//text()')
            l.add_value('pubDate', pubDate)
            l.add_value('source', 'bbc')

            yield l.load_item()
        else:
            next

class CbnSpider(scrapy.Spider):
    name = 'cbn'

    start_urls = [
        "http://www1.cbn.com/cbnnews/world/feed"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath("//channel/item"):

           request = scrapy.Request(item.xpath('(link|loc)//text()').extract_first(),
                                 callback=self.parse_page)
           request.cb_kwargs['title'] = item.xpath('title//text()').extract_first()
           request.cb_kwargs['description'] = item.xpath('(desc|description)//text()').extract_first()
           request.cb_kwargs['pubDate'] = item.xpath('(date|pubDate|publication_date)//text()').extract_first()
           request.cb_kwargs['author'] = item.xpath('(author|creator)//text()').extract_first()
           yield request

    def parse_page(self, response, title, description, pubDate, author):

        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//h1[contains(@class, "page-title")]//text()')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_value('description', description)
            l.add_xpath('author', '//div[contains(@property,"author")]/a//text()')
            l.add_xpath('content', '//div[contains(@class, "field-item")]//p//text()')
            l.add_value('pubDate', pubDate)
            l.add_value('source', 'cbn')

            yield l.load_item()
        else:
            next

class CnnSpider(scrapy.Spider):
    name = 'cnn'

    start_urls = [
        "http://rss.cnn.com/rss/edition_world.rss"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath("//channel/item"):

           request = scrapy.Request(item.xpath('link//text()').extract_first(),
                                 callback=self.parse_page)
           request.cb_kwargs['title'] = item.xpath('title//text()').extract_first()
           request.cb_kwargs['description'] = item.xpath('(desc|description)//text()').extract_first()
           request.cb_kwargs['pubDate'] = item.xpath('(date|pubDate)//text()').extract_first()
           request.cb_kwargs['author'] = item.xpath('(author|creator)//text()').extract_first()
           yield request

    def parse_page(self, response, title, description, pubDate, author):

        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//meta[contains(@property, "og:title")]//@content')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_value('description', description)
            l.add_xpath('author', '//meta[contains(@name, "author")]//@content')
            l.add_xpath('content', '//div[contains(@class, "zn-body__paragraph") or '
                                    'contains(@class, "BasicArticle") or'
                                    'contains(@class, "Paragraph__component")]//text()')
            l.add_xpath('content', '//div[contains(@class, "zn-body__paragraph")]//h3//text()')
            l.add_value('pubDate', pubDate)
            l.add_value('source', 'cnn')

            yield l.load_item()
        else:
            next

class France24Spider(scrapy.Spider):
    name = 'france24'

    start_urls = [
        "https://www.france24.com/en/rss"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath("//channel/item"):

           request = scrapy.Request(item.xpath('link//text()').extract_first(),
                                 callback=self.parse_page)
           request.cb_kwargs['title'] = item.xpath('title//text()').extract_first()
           request.cb_kwargs['description'] = item.xpath('(desc|description)//text()').extract_first()
           request.cb_kwargs['pubDate'] = item.xpath('(date|pubDate)//text()').extract_first()
           request.cb_kwargs['author'] = item.xpath('(author|creator)//text()').extract_first()
           yield request

    def parse_page(self, response, title, description, pubDate, author):

        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//meta[contains(@property, "og:title")]//@content')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_value('description', description)
            l.add_value('author', author)
            l.add_xpath('content', '//article//p//text()')
            l.add_value('pubDate', pubDate)
            l.add_value('source', 'france24')

            yield l.load_item()
        else:
            next

class LatimesSpider(scrapy.Spider):
    name = 'latimes'

    start_urls = [
        "https://www.latimes.com/world/rss2.0.xml"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath("//channel/item"):

           request = scrapy.Request(item.xpath('link//text()').extract_first(),
                                 callback=self.parse_page)
           request.cb_kwargs['title'] = item.xpath('title//text()').extract_first()
           request.cb_kwargs['description'] = item.xpath('(desc|description)//text()').extract_first()
           request.cb_kwargs['pubDate'] = item.xpath('(date|pubDate)//text()').extract_first()
           request.cb_kwargs['author'] = item.xpath('(author|creator)//text()').extract_first()
           yield request

    def parse_page(self, response, title, description, pubDate, author):

        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':

            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//*//h1[contains(@class, "headline")]//text()')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_value('description', description)
            l.add_value('author', author)
            l.add_xpath('content', '//div[contains(@class, "articleBody")]//p//text()')
            l.add_value('pubDate', pubDate)
            l.add_value('source', 'latimes')

            yield l.load_item()
        else:
            next

class NytimesSpider(scrapy.Spider):
    name = 'nytimes'

    start_urls = [
        'https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml',
        'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
    ]

    def parse(self, response):
        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath("//channel/item"):

           request = scrapy.Request(item.xpath('link//text()').extract_first(),
                                 callback=self.parse_page)
           request.cb_kwargs['title'] = item.xpath('title//text()').extract_first()
           request.cb_kwargs['description'] = item.xpath('(desc|description)//text()').extract_first()
           request.cb_kwargs['pubDate'] = item.xpath('(date|pubDate)//text()').extract_first()
           request.cb_kwargs['author'] = item.xpath('(author|creator)//text()').extract_first()
           yield request


    def parse_page(self, response, title, description, pubDate, author):
        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//*//h1//text()')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_value('description',description)
            l.add_value('author', author)
            l.add_xpath('content', '//section[contains(@name, "articleBody")]//p//text()')
            l.add_value('pubDate', pubDate)
            l.add_value('source', 'nytimes')

            yield l.load_item()
        else:
            next

class ObserverSpider(scrapy.Spider):
    name = 'observer'

    start_urls = [
        "https://observer.com/",
        "https://observer.com/international-politics/",
        "https://observer.com/national-politics/",
        "https://observer.com/politics/editorials/",
        "https://observer.com/technology/",
        "https://observer.com/startups/",
        "https://observer.com/national-security/"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath('//a[contains(@class, "module-entry-full-anchor")]/@href').extract():

            request = scrapy.Request(response.urljoin(item), callback=self.parse_page)
            request.cb_kwargs['title'] = response.xpath('//h2[contains(@class, "module-entry-title")]//text()').extract_first()
            #request.cb_kwargs['description'] = response.xpath('//a[contains(@class, "Component-asBlock")]//text()').extract_first()
            #request.cb_kwargs['pubDate'] = response.xpath('//span[contains(@class, "Timestamp")]/@data-source').extract_first()
            request.cb_kwargs['author'] = response.xpath('//div[contains(@class, "module-entry-author")]//text()').extract_first()
            yield request

    def parse_page(self, response, title, author):

        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            title = response.xpath('//h1[contains(@class, "entry-title")]//text()').extract_first()
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//h1[contains(@class, "entry-title")]//text()')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_xpath('description', '//meta[contains(@name, "description")]//@content')
            l.add_xpath('author', '//a[contains(@rel, "author")]//text()')
            l.add_xpath('content', '//div[contains(@itemprop, "articleBody") or'
                                          'contains(@class, "post-content")]//p//text()')
            l.add_xpath('pubDate', '//article/@data-date')
            l.add_value('source', 'theobserver')

            yield l.load_item()

class ReutersSpider(scrapy.Spider):
    name = 'reuters'

    start_urls = [
        "http://feeds.reuters.com/Reuters/worldNews"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath("//channel/item"):

           request = scrapy.Request(item.xpath('link//text()').extract_first(),
                                 callback=self.parse_page)
           request.cb_kwargs['title'] = item.xpath('title//text()').extract_first()
           request.cb_kwargs['description'] = item.xpath('(desc|description)//text()').extract_first()
           request.cb_kwargs['pubDate'] = item.xpath('(date|pubDate)//text()').extract_first()
           request.cb_kwargs['author'] = item.xpath('(author|creator)//text()').extract_first()
           yield request

    def parse_page(self, response, title, description, pubDate, author):
        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//h1[contains(@class, "headline")]//text()')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_value('description', description)
            #l.add_xpath('author', '//*[contains(@href,"journalists")]//text()')
            l.add_xpath('author', '//meta[contains(@name, "Author")]//@content')
            l.add_xpath('content', '//div[contains(@class, "StandardArticleBody") or'
                                        'contains( @class , "Attribution_attribution")]/p//text()')
            l.add_xpath('content', '//div[contains(@class, "StandardArticleBody")]/h3//text()')
            #l.add_xpath('content', '//div[contains(@class, "paragraph__component BasicArticle")]//text()')
            l.add_value('pubDate', pubDate)
            l.add_value('source', 'reuters')

            yield l.load_item()
        else:
            next

class TelegraphSpider(scrapy.Spider):
    name = 'telegraph'

    start_urls = [
        "http://www.telegraph.co.uk/rss.xml",
        "http://www.telegraph.co.uk/news/rss.xml",
        "http://www.telegraph.co.uk/politics/rss.xml",
        "http://www.telegraph.co.uk/technology/rss.xml",
        "http://www.telegraph.co.uk/business/rss.xml",
        "http://www.telegraph.co.uk/opinion/rss.xml"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath("//channel/item"):

           request = scrapy.Request(item.xpath('link//text()').extract_first(),
                                 callback=self.parse_page)
           request.cb_kwargs['title'] = item.xpath('title//text()').extract_first()
           request.cb_kwargs['description'] = item.xpath('(desc|description)//text()').extract_first()
           request.cb_kwargs['pubDate'] = item.xpath('(date|pubDate)//text()').extract_first()
           request.cb_kwargs['author'] = item.xpath('(author|creator)//text()').extract_first()
           yield request

    def parse_page(self, response, title, description, pubDate, author):
        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//meta[contains(@property, "og:title")]//@content')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_xpath('description', '//meta[contains(@name, "description")]//@content')
            l.add_xpath('author', '//meta[contains(@name, "author")]//@content')
            l.add_xpath('content', '//div[contains(@class, "article-body")]//p//text()')
            l.add_xpath('content', '//h3//text()')
            l.add_value('pubDate', pubDate)
            l.add_value('source', 'telegraph')

            yield l.load_item()
        else:
            next

class TheguardianSpider(scrapy.Spider):
    name = 'theguardian'

    start_urls = [
        "https://www.theguardian.com/world/rss"
    ]
    def parse(self, response):
        # from https://scrapy.ninja/en/web-scraping-in-python-using-scrapy-with-multiple-examples/
        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath("//channel/item"):

           request = scrapy.Request(item.xpath('link//text()').extract_first(),
                                 callback=self.parse_page)
           request.cb_kwargs['title'] = item.xpath('title//text()').extract_first()
           request.cb_kwargs['description'] = item.xpath('(desc|description)//text()').extract_first()
           request.cb_kwargs['pubDate'] = item.xpath('(date|pubDate)//text()').extract_first()
           request.cb_kwargs['author'] = item.xpath('(author|creator)//text()').extract_first()
           yield request

    def parse_page(self, response, title, description, pubDate, author):
        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//meta[contains(@property, "og:title")]//@content')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_value('description',description)
            l.add_value('author', author)
            l.add_xpath('content', '//div[contains(@itemprop, "articleBody")]//p//text()')
            l.add_value('pubDate', pubDate)
            l.add_value('source', 'theguardian')

            yield l.load_item()
        else:
            next

class ThetimesSpider(scrapy.Spider):
    name = 'thetimes'

    start_urls = [
        "https://www.times-series.co.uk/news/rss/"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath("//channel/item"):

           request = scrapy.Request(item.xpath('link//text()').extract_first(),
                                 callback=self.parse_page)
           request.cb_kwargs['title'] = item.xpath('title//text()').extract_first()
           request.cb_kwargs['description'] = item.xpath('(desc|description)//text()').extract_first()
           request.cb_kwargs['pubDate'] = item.xpath('(date|pubDate)//text()').extract_first()
           request.cb_kwargs['author'] = item.xpath('(author|creator)//text()').extract_first()
           yield request

    def parse_page(self, response, title, description, pubDate, author):
        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'website':
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//meta[contains(@property, "og:title")]//@content')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_value('description', description)
            #l.add_value('author', '')
            l.add_xpath('author', '//*//a[contains(@href,"author")]//text()')
            l.add_xpath('content', '//div[contains(@class, "article-body")]//p//text()')
            l.add_value('pubDate', pubDate)
            l.add_value('source', 'thetimes')

            yield l.load_item()
        else:
            next

class ThetimesUKSpider(scrapy.Spider):
    name = 'thetimesUK'

    start_urls = [
        "https://www.thetimes.co.uk/"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath('//h3//@href').extract():

            request = scrapy.Request(response.urljoin(item), callback=self.parse_page)
            yield request

    def parse_page(self, response):
        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            link = response.url
            file_id = hashlib.md5(link.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//meta[contains(@property, "og:title")]//@content')
            l.add_value('file_id', file_id)
            l.add_xpath('title', '//h1[contains(@role, "heading")]//text()')
            l.add_value('link', link)
            #l.add_value('description', 'None')
            l.add_xpath('description', '//meta[contains(@property, "description")]//@content')
            #l.add_xpath('author', '//a[contains(@href, "/profile/")]//text()')
            l.add_xpath('author', '//meta[contains(@name, "author")]//@content')
            l.add_xpath('content', '//article[contains(@role, "article")]//p//text()')
            l.add_xpath('pubDate', '//time/@datetime')
            l.add_value('source', 'thetimesUK')

            yield l.load_item()
        else:
            next

class TimesofindiaSpider(scrapy.Spider):
    name = 'timesofindia'

    start_urls = [
        "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath("//channel/item"):

           request = scrapy.Request(item.xpath('link//text()').extract_first(),
                                 callback=self.parse_page)
           request.cb_kwargs['title'] = item.xpath('title//text()').extract_first()
           request.cb_kwargs['description'] = item.xpath('(desc|description)//text()').extract_first()
           request.cb_kwargs['pubDate'] = item.xpath('(date|pubDate)//text()').extract_first()
           request.cb_kwargs['author'] = item.xpath('(author|creator)//text()').extract_first()
           yield request

    def parse_page(self, response, title, description, pubDate, author):
        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//meta[contains(@property, "og:title")]//@content')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_xpath('description', '//meta[contains(@name, "description")]//@content')
            l.add_value('author', author)
            l.add_xpath('content', '//div[contains(@class, "_3WlLe")]//text()')
            l.add_value('pubDate', pubDate)
            l.add_value('source', 'timesofindia')

            yield l.load_item()
        else:
            next

class ViceSpider(scrapy.Spider):
    name = 'vice'

    start_urls = [
        "https://www.vice.com/en_us",
        "https://www.vice.com/en_us/section/news",
        "https://www.vice.com/en_us/section/tech",
        "https://www.vice.com/en_us/section/music",
        "https://www.vice.com/en_us/section/food",
        "https://www.vice.com/en_us/section/health"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath('//a[contains(@class, "heading-hover")]//@href').extract():
            request = scrapy.Request(response.urljoin(item), callback=self.parse_page)
            yield request

    def parse_page(self, response):

        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            title = response.xpath('//meta[contains(@property, "og:title")]//@content').extract_first()
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//meta[contains(@property, "og:title")]//@content')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_xpath('description', '//meta[contains(@property, "og:description")]//@content')
            l.add_xpath('author', '//meta[contains(@property, "article:author")]//@content')
            l.add_xpath('content', '//div[contains(@data-type, "body-text")]//p//text()')
            l.add_xpath('pubDate', '//meta[contains(@name, "datePublished")]//@content')
            l.add_value('source', 'vice')

            yield l.load_item()
        else:
            next

class WiredSpider(scrapy.Spider):
    name = 'wired'

    start_urls = [
        "https://www.wired.com",
        "https://www.wired.com/category/business/"
    ]

    def parse(self, response):

        # to deal with xml tags eg <dc:creator>
        response.selector.remove_namespaces()

        for item in response.xpath('//a[contains(@to, "/story/")]//@href').extract():
            request = scrapy.Request(response.urljoin(item), callback=self.parse_page)
            yield request

    def parse_page(self, response):

        x = response.xpath('//meta[contains(@property, "og:type")]//@content').extract_first()

        if x in 'article':
            title = response.xpath('//meta[contains(@property, "og:title")]//@content').extract_first()
            file_id = hashlib.md5(title.encode('utf-8')).hexdigest()

            l = ItemLoader(item=NewsArticle(), response=response)
            l.add_xpath('headline', '//meta[contains(@property, "og:title")]//@content')
            l.add_value('file_id', file_id)
            l.add_value('title', title)
            l.add_value('link', response.url)
            l.add_xpath('description', '//meta[contains(@property, "og:description")]//@content')
            l.add_xpath('author', '//meta[contains(@name, "author")]//@content')
            l.add_xpath('content', '//div[contains(@class, "body")]//p//text()')
            l.add_xpath('pubDate', '//time//text()')
            l.add_value('source', 'wired')

            yield l.load_item()
        else:
            next