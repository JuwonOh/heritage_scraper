from .utils import get_soup
from .utils import now
from dateutil.parser import parse

def parse_page(url):
    """
    Argument
    --------
    url : str
        Web page url

    Returns
    -------
    json_object : dict
        JSON format web page contents
        It consists with
            title : article title
            time : article written time
            content : text with line separator \\n
            url : web page url
            scrap_time : scrapped time
    """
    try:
        if 'report/' in url:
            return parse_report(url)
        if '/commentary/' in url:
            return parse_commentary(url)
    except Exception as e:
        print(e)
        print('Parsing error from {}'.format(url))
        return None

def parse_report(url):

    def parse_title(soup):
        title = soup.find('h1', class_='headline article-headline')
        if not title:
            return ''
        return title.text

    def parse_author(soup):
        author = soup.find('a', rel='bookmark')
        if not author:
            return 'no author'
        return author.text

    def parse_date(soup):
        date = soup.find('div', class_= 'article-general-info')
        if not date:
            return ''
        return parse(date.text[:-35])
    def parse_tag(soup):
        tag = soup.find('div', class_='impact__eyebrow article__eyebrow')
        if not tag:
            return 'no tag'
        return tag.find('a').text

    def parse_content(soup):
        content = soup.find('section', class_= 'article-summary summary more-bottom')
        if not content:
            return ''
        return content.text

    def parse_publication_link(soup):
        a =  soup.find_all('a', target='_blank')
        for b in a:
            if 'sites/default/files/' in b.attrs['href']:
                return b.attrs['href']
            if 'print()' in b.attrs['href']:
                return 'no link'

    soup = get_soup(url)
    temp_content_url = parse_publication_link(soup)

    if 'https:' not in temp_content_url:
        content_url = 'https://www.heritage.org' + temp_content_url
    else:
        content_url = temp_content_url
    return {
        'url': url,
        'title': parse_title(soup),
        'date': parse_date(soup),
        'author': parse_author(soup),
        'content': parse_content(soup),
        'content_url': content_url,
        'tag' : parse_tag(soup),
        'scraping_date' : now()
        }

def parse_commentary(url):
    def parse_author(soup):
        author = soup.find('a', class_='author-card__name')
        if not author:
            return ''
        return author.text

    def parse_title(soup):
        title = soup.find('h1', class_='commentary__headline headline')
        if not title:
            return ''
        return title.text

    def parse_tag(soup):
        tag = soup.find('div', class_='commentary__eyebrow article__eyebrow')
        if not tag:
            return 'no tag'
        return tag.find('a').text

    def parse_date(soup):
        date = soup.find('div', class_= 'article-general-info')
        if not date:
            return ''
        return parse(date.text[:-12])

    def parse_content(soup):
        content = soup.find('div', class_= 'article__body-copy')
        if not content:
            return ''
        return content.text

    soup = get_soup(url)

    return {
        'url': url,
        'title': parse_title(soup),
        'date': parse_date(soup),
        'content': parse_content(soup),
        'author': parse_author(soup),
        'tag' : parse_tag(soup),
        'scraping_date' : now()
    }
