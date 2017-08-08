"""
Twittrendから情報収集して
NAVERまとめにログインして記事を投稿する。
＊画像認証がある
"""

import twitter_trend

import trend_matome_publish
import datetime

import twitter_tweet
import subprocess

from data import *
import queue
import time

import pickle

AUTO = True
TIME_TABLE = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
SLEEP_SEC = (24 + TIME_TABLE[0] - TIME_TABLE[-1] - 1) * 60 * 60
WRITE_ARTICLE = False

# TODO: 「何時半」の対応
"""
今のHOURを小数で表す。
10〜10.5のとき、10.5〜11のとき、…といった条件で投稿を決める。
簡単だ。
"""
TIME_TABLE = [10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5,
              15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5,
              21, 21.5, 22, 22.5, 23]
TIME_NEXT = [10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5,
             15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5,
             21, 21.5, 22, 22.5, 23, 10]


if __name__ == "__main__":

    # トレンドがかぶらないように蓄えておくためのリスト。
    with open(PATH_TREND + 'categ_list.pickle', mode='rb') as f:
        categ_list = pickle.load(f)
        print('トレンド履歴:', categ_list)

    # スケジュール用のキューを作成
    schedule = queue.Queue()
    for t in TIME_TABLE:
        schedule.put(t)

    # ひとつ先のスケジュール
    schedule_n = queue.Queue()
    for t_n in TIME_NEXT:
        schedule_n.put(t_n)

    # 現在時刻の取得(日本時間)
    today = datetime.datetime.today()
    # 時間をfloatで表す
    hour = today.hour + today.minute / 60

    # 記事を書き続けるためのループ
    while True:

        # 記事の投稿に失敗した場合、WRITE_ARTICLEはTrueのまま
        if WRITE_ARTICLE is False:
            # スケジュールを次に回す
            t = float(schedule.get())
            schedule.put(t)

            # ひとつ先のスケジュールを次に回す
            t_n = float(schedule_n.get())
            schedule_n.put(t_n)

        # 指定の時刻が来るまでここで待機する
        while WRITE_ARTICLE is False:
            WRITE_ARTICLE = True
            # 現在時刻の取得(日本時間)
            today = datetime.datetime.today()
            # 時間をfloatで表す
            hour = today.hour + today.minute / 60
            print('現在:%f 待ち:%f, %f' % (hour, t, t_n))

            # 今日の分を全て終えた場合
            if t == TIME_TABLE[0] and TIME_TABLE[-1] <= hour:
                print('今日の分を終えたので寝ます。')
                categ_list = []
                WRITE_ARTICLE = False
                time.sleep(SLEEP_SEC)
                print('おはようございます。')
                continue

            # 記事を書き始める時刻かどうか見極める
            if t <= hour < t_n:
                print(str(t) + '時の記事を書き始めます。')
            elif hour < t:
                print('待ち')
                WRITE_ARTICLE = False
                time.sleep(600)

        # [試験段階のみ] 見逃した分のTIME_TABLEを次に進める。
        if t_n < hour:
            print(str(t) + '時を見送ります。')
            WRITE_ARTICLE = False
            continue

        """
        以下、投稿の開始
        """

        # フォルダの掃除
        print(PATH_TREND_DEBUG + '内を空にします')
        cmd = 'rm ' + PATH_TREND_DEBUG + '*.png'
        print(cmd)
        subprocess.call(cmd, shell=True)

        # フォルダの掃除
        print(PATH_TREND_SRC + '内を空にします')
        cmd = 'rm ' + PATH_TREND_SRC + '*.png'
        print(cmd)
        subprocess.call(cmd, shell=True)

        twitter_tweet.tweet_sentence("トレンドをチェックします。")

        while True:
            # トレンドを確認し必要な情報を獲得する
            Tre = twitter_trend.TwitterTrend()

            categ_name = Tre.categ_name
            img_file = Tre.image_file
            data_list = Tre.tweet_url_list

            if categ_name in categ_list:
                print('カテゴリ名がかぶりました。')
                continue
            elif not img_file:
                print('画像が取得できませんでした。')
                categ_list.append(categ_name)
                continue
            else:
                categ_list.append(categ_name)
                # カテゴリ履歴をpickleにする
                with open(PATH_TREND + 'categ_list.pickle', mode='wb') as f:
                    pickle.dump(categ_list, f)
                break

        today_str = str(today.month) + '月' + str(today.day) + '日'

        title = "【" + today_str + "】「" + categ_name + "」の話題ツイートをまとめてみた【Twitterトレンド】"
        twitter_tweet.tweet_sentence("タイトルは\"" + title + "\"に決定しました。")

        Matome = trend_matome_publish.MatomePublish(title, img_file, data_list)

        matome_url = Matome.matome_url

        if Matome.status is True:
            twitter_tweet.tweet_sentence("完成しました。URL→" + matome_url)
            # TODO: 拡散用ツイート
            # twitter_tweet.p_tweet_sentence(title + '\n' + matome_url)
            WRITE_ARTICLE = False
        else:
            # 投稿に失敗したのでもう一度挑戦する
            WRITE_ARTICLE = True

        if AUTO is False:
            break


