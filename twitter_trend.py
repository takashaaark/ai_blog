"""
Twittrendから情報をいただく

"""

import urllib.request as req
from bs4 import BeautifulSoup
import random

from sys import stdin
import pickle

from data import *

URL = 'http://twittrend.jp/'
RELOAD_TREND = True  # あんまり接続したくないときにFalse
RELOAD_TWEET = True  # あんまり接続したくないときにFalse
TRENDS_NUM = 10


class TwitterTrend(object):
    def __init__(self):

        self.categ_name = ''
        self.tweet_url_list = []
        self.image_file = ''

        html = req.urlopen(URL).read()
        soup = BeautifulSoup(html, "html.parser")

        if RELOAD_TREND is True:
            # トレンドを上位 TRENDS_NUM 個取得
            tr_info = soup.find_all("p", class_="trend")[0:TRENDS_NUM]

            trends = []
            # それぞれの順位、リンク、名称を取得
            for i in range(TRENDS_NUM):
                trend = dict()
                trend['rank'] = int(tr_info[i].find("span").string[0:-1])
                trend['url'] = str(tr_info[i].find("a").get("href"))
                trend['name'] = str(tr_info[i].find("a").string)
                trends.append(trend)

            with open(PATH_TREND + 'trends.pickle', mode='wb') as f:
                pickle.dump(trends, f)
        else:
            with open(PATH_TREND + 'trends.pickle', mode='rb') as f:
                trends = pickle.load(f)

        print(trends)

        # TODO: 知能的にトレンドを選択する機構を作る。強化学習など使えたら素敵。

        # とりあえず適当に選ぶ
        chosen_trend = random.choice(trends)
        self.categ_name = chosen_trend['name']
        print('カテゴリは', self.categ_name, 'に決定しました。')

        if RELOAD_TWEET is True:
            chosen_html = req.urlopen(chosen_trend['url']).read()
            chosen_soup = BeautifulSoup(chosen_html, "html.parser")
            with open(PATH_TREND + 'chosen_soup.html', mode='w', encoding='utf-8') as fw:
                fw.write(chosen_soup.prettify())
        else:
            chosen_soup = BeautifulSoup(open(PATH_TREND + 'chosen_soup.html', encoding='utf-8'), 'html.parser')

        # トレントページ上のツイートを全て取得
        tw_info = chosen_soup.find_all("div", class_="js-stream-tweet")

        # トレントページに表示されているツイートのリンクリストを作成
        for i, tw in enumerate(tw_info):
            # ツイートのURLををひとつずつ取得
            perma_path = tw['data-permalink-path']
            tweet_url = 'https://twitter.com' + perma_path
            self.tweet_url_list.append(tweet_url)
            # 最大20ツイートまでに限定する
            if i >= 20:
                break
        print(self.tweet_url_list)

        # twi_tre_src を空にする

        # 記事のタイトル画像をツイートから拾う
        img_info = chosen_soup.find_all("img")
        savename_list = []
        for i, img in enumerate(img_info):
            if 'src' in img.attrs:
                img_url = img.attrs['src']
                if 'https://pbs.twimg.com/media/' in img_url:
                    savename = PATH_TREND_SRC + 'small_image' + str(i) + '.png'
                    req.urlretrieve(img_url, savename)
                    savename_list.append(savename)
        print(savename_list)

        # TODO: もうちょっとカッコよく書きたい
        if not savename_list:
            pass
        else:
            self.image_file = random.choice(savename_list)
            print(self.image_file + 'に決定')

            # TODO: 画像のトリミング


if __name__ == '__main__':

    Tre = TwitterTrend()














