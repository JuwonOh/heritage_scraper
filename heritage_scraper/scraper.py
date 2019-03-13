import re
import time
from dateutil import parser
from datetime import datetime
from .parser import parse_page
from .utils import get_soup
from .utils import report_dateformat
from .utils import user_dateformat
from .utils import commentary_dateformat
from .utils import strf_to_datetime

def is_matched(url):
    for pattern in patterns:
        if pattern.match(url):
            return True
    return False

patterns = [
    re.compile('https://www.heritage.org/[\w]+')]
url_kor = 'https://www.heritage.org/search?contains=korea&type=All&date_offset=&range_start=&range_end=&page={}'
url_kor_yield = 'https://www.heritage.org/search?contains=korea&range_start={}&range_end={}&type=All&date_offset=&page={}'

def yield_latest_article(begin_date, end_date, max_num=10, sleep=1.0):
    """
    Artuments
    ---------
    begin_date : str
        eg. 2018-07-01
    end_date :str
        eg. 2019-03-31
    max_num : int
        Maximum number of news to be scraped
    sleep : float
        Sleep time. Default 1.0 sec

    It yields
    ---------
    news : json object
    """

    # prepare parameters
    d_begin = strf_to_datetime(begin_date, user_dateformat)
    end_page = 72
    n_news = 0
    outdate = False

    for page in range(0, end_page+1):

        # check number of scraped news
        if n_news >= max_num or outdate:
            break

        # get urls
        links_all= []
        url = url_kor_yield.format(begin_date, end_date, page)
        soup = get_soup(url)
        sub_links = soup.find_all('a', class_= 'result-card__title js-hover-target')
        links = ['https://www.heritage.org' + i.attrs['href'] for i in sub_links]
        links_all += links
        links_all = [url for url in links_all if is_matched(url)]

        # scrap
        for url in links_all:
            news_json = parse_page(url)
            # yield
            yield news_json

            # check number of scraped news
            n_news += 1
            if n_news >= max_num:
                break
            time.sleep(sleep)


def get_article_urls(begin_page=0, end_page=3, verbose=True):
    """
    Arguments
    ---------
    begin_page : int
        Default is 1
    end_page : int
        Default is 3
    verbose : Boolean
        If True, print current status

    Returns
    -------
    links_all : list of str
        List of urls
    """

    links_all = []
    for page in range(begin_page, end_page+1):
        url = url_kor.format(page)
        soup = get_soup(url)
        sub_links = soup.find_all('a', class_= 'result-card__title js-hover-target')
        links = ['https://www.heritage.org' + i.attrs['href'] for i in sub_links]
        links_all += links
        links_all = [url for url in links_all if is_matched(url)]

    return links_all
