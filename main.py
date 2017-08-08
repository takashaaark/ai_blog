"""
食べログから情報収集して
NAVERまとめにログインして記事を投稿する。
＊画像認証がある
"""

import tabelog_search
import matome_publish
import title_maker

import twitter_tweet

import subprocess
from data import *

if __name__ == "__main__":

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

    twitter_tweet.tweet_sentence("完成だ。")


