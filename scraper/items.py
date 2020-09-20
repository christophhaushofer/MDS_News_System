# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Compose
from w3lib.html import remove_tags, replace_entities, replace_escape_chars
import re
import dateparser

def date_convert(value):

    dateparserSettings = {'RETURN_AS_TIMEZONE_AWARE': True, }

    value = re.sub(r'^([a-zA-Z]{3}, [0-9]{2} [a-zA-Z]{3} [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2})\.[0-9]+', r'\1', value)

    try:
        nx = dateparser.parse(value, settings=dateparserSettings)
    except TypeError:
        nx = None
    if not nx:
        print(('Failed to parse date from: ' + value))
    return nx

class NewsItem(scrapy.Item):
    file_id = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    headline = scrapy.Field(
        input_processor=Compose(Join(' '),
                                lambda x: replace_escape_chars(x, replace_by=' '),
                                lambda x: re.sub('<[^>]*>', '', x),
                                lambda x: re.sub('\n', '', x),
                                lambda x: re.sub(' +', ' ', x),
                                lambda x: x.strip(),
                                replace_entities,
                                ),
        output_processor=TakeFirst(),
    )
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    link = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    description = scrapy.Field(
        input_processor=MapCompose(
                            remove_tags,
                            lambda x: re.sub('Continue reading...', '', x),
                            lambda x: x.strip(),
                                   ),
        output_processor=Join(),
    )
    content = scrapy.Field(
        input_processor=Compose(Join(' '),
                             lambda x: replace_escape_chars(x, replace_by=' '),
                             lambda x: re.sub('<[^>]*>', '', x),
                             lambda x: re.sub(' +', ' ', x),
                             replace_entities,
                            ),
        output_processor=TakeFirst(),
    )
    author = scrapy.Field(
        input_processor=MapCompose(
                                lambda x: re.sub(" and ", ', ', x),
                                lambda x: re.sub(r'.*[Bb]y ', r'', x).strip(),
                                lambda x: x.split(' in ')[0],
                                replace_entities,
                                ),
        output_processor=Join(', '),
    )
    pubDate = scrapy.Field(
        input_processor=MapCompose(date_convert),
        output_processor=TakeFirst()
    )
    source = scrapy.Field(
        input_processor=MapCompose(
                                remove_tags,
                                lambda x: re.sub('\r\n +SOURCE:\r\n +', '', x),
                                lambda x: re.sub(' +', ' ', x),
                                lambda x: re.sub(" and ", ', ', x),
                                lambda x: re.sub(" with ", ', ', x),
                                lambda x: re.sub('(?<!:)[()]', '', x),
                                lambda x: re.sub('<[^>]*>', '', x),
                                replace_entities,
                                ),
        output_processor=Join(),
    )
