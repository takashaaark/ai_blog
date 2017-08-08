"""
地名を与えたらタイトルをつくってくれる
"""

from random import choice
from datetime import datetime


# 記事の内容
def title_maker(pref_name, target_name):

    year = str(datetime.now().year)

    list_head = [pref_name, '絶対うまい', '絶品', '決定版', '幸せ', '美味い', 'よだれ', 'ロマン', '伝説の店']
    list_word1 = ['生きているうちに', '死ぬまでに', '知らなきゃ損？', 'レビュワーおすすめの', 'レビュワー大絶賛！']
    list_word2 = ['必ず', '絶対に', '本気で', '全力で']
    list_word3 = ['いきたい', '行きたい', '訪れるべき', '訪れたい', '行くべき', '行っておくべき',
                  '食べたい', '食べるべき', '食べに行きたい']
    list_word4 = ['', '!', '!!', '！']
    list_10sen = ['の名店10選', 'の有名店10選', 'の名店ベスト10', 'の有名店ベスト10']
    list_tail = [year, year+'版', year+'年', '最新情報', '最新']

    head = '【' + choice(list_head) + '】'
    words_a = choice(list_word1) + choice(list_word2) + choice(list_word3) + choice(list_word4)
    words_b = choice(list_10sen) + choice(list_word4)
    tail = '【' + choice(list_tail) + '】'

    title = head + words_a + target_name + words_b + tail

    return title


if __name__ == "__main__":
    print(title_maker('滋賀', '草津'))
