# encoding: utf-8


import sys

from workflow import Workflow


def search_movie(wf, r):
    """搜索电影"""

    result = r.json()
    if result:
        if len(result['subjects']):
            subjects = result['subjects']
            for subject in subjects:
                average = subject['rating']['average']
                title = subject['title']
                alt = subject['alt']
                year = subject['year']
                casts = subject['casts']
                actors = ''
                if len(casts):
                    for cast in casts:
                        actors += cast['name'] + ' / '
                wf.add_item(title=title + ' (' + year + ')', subtitle=u'评分:' + str(average) + '\t' + actors, arg=alt,
                            valid=True, icon='image/movie_item.png')
        else:
            wf.add_item(title=u'查询不到相关信息')


def playing_movie(wf, soup):
    playing_div = soup.find('div', id='nowplaying')
    all_li = playing_div.find_all('li', class_='list-item')
    for li in all_li:
        movie_name = li['data-title']
        movie_score = li['data-score']
        movie_len = li['data-duration']
        movie_votecount = li['data-votecount']
        movie_detail_url = li.find('a')['href']
        actors = li['data-actors']
        subtitle = movie_len + u'\t评分:' + movie_score + '\t' + actors
        wf.add_item(title=movie_name, subtitle=subtitle, arg=movie_detail_url, valid=True, icon='image/movie.png')


def main(wf):
    from bs4 import BeautifulSoup
    import requests

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    # 获取参数
    param = (wf.args[0] if len(wf.args) else '').strip().encode('utf-8')

    if param:
        search_url = 'https://api.douban.com/v2/movie/search'
        params = {'q': param, 'start': 0, 'count': 20}
        r = requests.get(search_url, headers=headers, params=params)
        search_movie(wf, r)
    else:
        url = 'https://movie.douban.com/cinema/nowplaying/'
        data = requests.get(url, headers=headers).content
        soup = BeautifulSoup(data, 'html.parser')
        playing_movie(wf, soup)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'])
    sys.exit(wf.run(main))
