## Heritage_scraper

미국의 싱크탱크인 헤리티지 재단(The Heritage Foundation, https://www.heritage.org)의 한국과 관련된 자료들을 받아오는 크롤러입니다. 검색한 url을 토대로 자료를 받고, 그걸 json으로 저장해 줍니다. 검색어 변경 기능은 차후에 추가할 예정입니다.

## User guide

크롤러의 파이썬 파일은 util.py, scraper.py, parser.py, downloader.py 그리고 scraping_latest_news.py 총 다섯가지로 구성되어 있습니다. 
util.py는 크롤링 한 파이썬의 beautifulsoup 패키지를 받아서 url내의 html정보를 정리하는 등 scraper가 필요한 기본적인 기능을 가지고 있습니다.
parser.py는 모아진 url리스트를 통해서 각 분석들의 제목/일자/내용 등의 문자, 시간 데이터들을 parsing 합니다.
scraper.py는 사이트내의 url 링크들을 get_soup함수를 통해 모아주고, parser를 통해서 json형식으로 변환시킵니다.
downloader.py는 reserch paper와 Brookings papers on economy activity article의 pdf파일을 다운로드 하는 파일입니다.
scraping_latest_news.py는 scraper.py를 통해 만들어진 json파일을 저장시켜줍니다. scraping_latest_news.py파일의 parameter는 다음과 같습니다.

Using Python script with arguments

| Argument name | Default Value | Note |
| --- | --- | --- |
| begin_date | 2018-07-01 | datetime YYYY-mm-dd |
| directory | ./output/ | Output directory |
| max_num | 1000 | Maximum number of news to be scraped |
| sleep | 1.0 | Sleep time for each news |
| verbose | False, store_true | If True use verbose mode |

만일 2018년 7월 1일부터 작성된 자료를 1000개까지 받고 싶다면 다음과 같이 실행코드를 입력해주시면 됩니다.

```
scraping_latest_news.py --begin_date 2018/07/01 --directory ./output --max_num 1000 --sleep 1.0
```
최근 순서대로 크롤링한 파일을 살펴보고 싶을때는 usage.ipynb를 사용하세요.

```
from heritage_scraper import yield_latest_article

begin_date = '2018-12-01'
end_date = '2019-03-31'
max_num = 10
sleep = 1.0

for i, json_obj in enumerate(yield_latest_article(begin_date, end_date, max_num, sleep)):
    title = json_obj['title']
    time = json_obj['date']
    print('[{} / {}] ({}) {}'.format(i+1, max_num, time, title))
```

```
[1 / 10] (2019-02-06 00:00:00) This Is No Time for an Artificial Peace in Korea
[2 / 10] (2018-12-26 00:00:00) My North Korea Prediction for 2019
[3 / 10] (2019-02-27 00:00:00) 6 Things Trump Should Demand of North Korea
[4 / 10] (2019-02-27 00:00:00) What a Denuclearization Agreement With North Korea Should Include
[5 / 10] (2019-02-22 00:00:00) Trump’s Big Challenge at the Upcoming North Korea Summit
[6 / 10] (2019-02-19 00:00:00) South Korea Survives Trump’s Stress Test
[7 / 10] (2019-02-22 00:00:00) Leveraging U.S. Law to Advocate for Human Rights in Talks with North Korea
[8 / 10] (2018-12-13 00:00:00) Trump Shouldn't Lower His Guard on North Korea
[9 / 10] (2019-02-21 00:00:00) Second U.S.–North Korea Summit Must Focus on Substance, Not Style
[10 / 10] (2019-02-11 00:00:00) Why Human Rights Must Be Raised at a Second Summit With North Korea
```

## 참고 코드

본 코드는 https://github.com/lovit/whitehouse_scraper를 참조하여 만들어졌습니다.
