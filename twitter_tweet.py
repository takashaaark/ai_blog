import json
from requests_oauthlib import OAuth1Session
from twitter_settings import *
from datetime import datetime


def send_secure_request(png_address):

    url_media = "https://upload.twitter.com/1.1/media/upload.json"
    url_text = "https://api.twitter.com/1.1/statuses/update.json"

    # OAuth認証 セッションを開始
    twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # 画像投稿
    files = {"media": open(png_address, 'rb')}
    req_media = twitter.post(url_media, files=files)

    # レスポンスを確認
    if req_media.status_code != 200:
        print("画像アップデート失敗: %s", req_media.text)
        exit()

    # Media ID を取得
    media_id = json.loads(req_media.text)['media_id']
    print("Media ID: %d" % media_id)

    # Media ID を付加してテキストを投稿
    target = 'takashaaark'
    message = '画像認証です。よろしく頼みます'
    text = '@' + target + ' ' + message
    params = {'status': text, "media_ids": [media_id]}
    req_media = twitter.post(url_text, params=params)

    # 再びレスポンスを確認
    if req_media.status_code != 200:
        print("テキストアップデート失敗: %s", req_media.text)
        exit()

    print("送信完了:", text)


def tweet_sentence(message):

    tweet_time = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    url_text = "https://api.twitter.com/1.1/statuses/update.json"

    # OAuth認証 セッションを開始
    twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    text = message + '\n' + tweet_time

    # Media ID を付加してテキストを投稿
    params = {'status': text}
    req_media = twitter.post(url_text, params=params)

    # 再びレスポンスを確認
    if req_media.status_code != 200:
        print("テキストアップデート失敗: %s", req_media.text)
        exit()

    print("TWEET:", message)


def p_tweet_sentence(message):
    """
    公開用ツイート
    """

    url_text = "https://api.twitter.com/1.1/statuses/update.json"

    # OAuth認証 セッションを開始
    twitter = OAuth1Session(P_CONSUMER_KEY, P_CONSUMER_SECRET, P_ACCESS_TOKEN, P_ACCESS_TOKEN_SECRET)

    text = message

    # Media ID を付加してテキストを投稿
    params = {'status': text}
    req_media = twitter.post(url_text, params=params)

    # 再びレスポンスを確認
    if req_media.status_code != 200:
        print("テキストアップデート失敗: %s", req_media.text)
        exit()

    print("TWEET:", message)


if __name__ == "__main__":
    pass
