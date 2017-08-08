"""
NAVERまとめにログインして記事を投稿する。
画像認証がある
"""

import tabelog_search
import matome_publish
import title_maker

import time
import twitter_tweet

from data import *
import subprocess

REST_HOUR = 0.75


if __name__ == "__main__":

    while True:
        print(PATH_TABELOG_DEBUG + '内を空にします')
        cmd = 'rm ' + PATH_TABELOG_DEBUG + '*.png'
        print(cmd)
        subprocess.call(cmd, shell=True)

        print(PATH_TABELOG_SRC + '内を空にします')
        cmd = 'rm ' + PATH_TABELOG_SRC + '*.png'
        print(cmd)
        subprocess.call(cmd, shell=True)

        twitter_tweet.tweet_sentence("仕事を始めるか")

        Tabe = tabelog_search.TabelogSearch()

        pref_name = Tabe.pref_name
        target_name = Tabe.target_name

        title = title_maker.title_maker(pref_name, target_name)
        twitter_tweet.tweet_sentence("タイトルは\"" + title + "\"に決めたぞ")

        img_file = Tabe.image_file
        data_list = Tabe.rank_list

        Matome = matome_publish.MatomePublish(title, img_file, data_list)

        twitter_tweet.tweet_sentence("完成だ。" + str(REST_HOUR) + "時間ほど休憩しよう")
        rest_sec = REST_HOUR * 60 * 60
        time.sleep(rest_sec)

