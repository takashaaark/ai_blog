"""
YouTubeの急上昇動画３つのタイトルをツイッターで呟くだけ
"""

import json
from requests_oauthlib import OAuth1Session
from twitter_settings import *
from datetime import datetime

import urllib.request as req
from bs4 import BeautifulSoup


class TwitterTrend(object):
    def __init__(self):
        pass


if __name__ == '__main__':

    # TwitterTrend()
    # OAuth認証 セッションを開始
    twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    #
    # twitter.get(trends)

    # ツイート投稿用のURL
    url = 'https://api.twitter.com/1.1/statuses/update.json'

    # OAuth認証
    # twitter = OAuth1Session(CK, CS, AT, AS)

    # youtubeの急上昇サイトへアクセス
    trend_html = req.urlopen('https://www.youtube.com/feed/trending')
    body = trend_html.read()

    # HTML をパースする
    soup = BeautifulSoup(body, 'lxml')

    # 急上昇サイトのclass属性を指定してスクレイピング
    msg = soup.find_all(class_='yt-uix-tile-link')

    status = 'youtube注目動画\n'

    # 急上昇サイトの上から3つの動画タイトルをstatus変数へ代入
    for i in range(0, 3):
        status += '・' + msg[i]['title'] + '\n'

        # ツイート本文
        params = {'status': status}

    # twitterに投稿
    req = twitter.post(url, params=params)

    # コンソールへも出力















