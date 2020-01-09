# encoding: utf-8


import sys

from workflow import Workflow


def search_movie(wf, result):
    """搜索电影"""
    
    if result:
        for item in result:
            if item.has_key('rating'):
                title = item['title']
                rating_value = item['rating']['value']
               
                movie_time = item['abstract'][item['abstract'].rfind('/')+1:len(item['abstract'])]
                actors = item['abstract_2']
                wf.add_item(title=title , subtitle=movie_time + '\t'  + str(rating_value) + '\t' + actors ,arg=item['url'],
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
    import douban

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    # 获取参数
    param = (wf.args[0] if len(wf.args) else '').strip().encode('utf-8')

    if param:
        r = douban.search(param)
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
