"""
食べログから情報をいただく

"""

import urllib.request as req
from bs4 import BeautifulSoup
from random import randint
from random import choice

from sys import stdin

from data import *

URL = 'https://tabelog.com/'


class TabelogSearch(object):
    def __init__(self):

        # 都道府県ページへのURLを取得
        self.pref_name, self.pref_url = self.get_prefecture_url()
        print('都道府県は', self.pref_name, 'に決定しました。')

        # 都道府県ページにアクセスし、絞り込みページへのURLを取得
        self.reco_name, self.reco_url = self.get_recommended_url()
        print('絞り込みは', self.reco_name, 'に決定しました')

        # ターゲットページ <- 絞り込みページ
        self.target_name, self.target_url = self.reco_name, self.reco_url
        # 画像の保存場所文字列の確保
        self.image_file = ''

        # ターゲットページにおけるランキング上位20を取得
        self.rank_list = self.get_ranking_list()

    def get_prefecture_url(self):
        """
        都道府県ページのURLを取得
        """
        # 都道府県リストを取得
        pref_list = self.get_prefecture_list()

        # 都道府県の番号を決定し、そのURLを取得
        pref_name, pref_url = self.choose_random(pref_list)

        return pref_name, pref_url

    @staticmethod
    def get_prefecture_list():
        """
        都道府県のリンクリストを取得
        """
        top_html = req.urlopen(URL).read()
        top_soup = BeautifulSoup(top_html, "html.parser")
        link_to_pref_a = top_soup.select("li.rsttop-search__pref-list-item > a")
        pref_list = []
        for a in link_to_pref_a:
            href = a.attrs["href"]
            title = a.string
            pref_list.append((title, href))
        return pref_list

    @staticmethod
    def choose_random(pref_list):
        """
        都道府県リストからランダムに１つ選ぶ。確認をとらない場合。
        """
        # 都道府県の番号をランダムに取得
        num = randint(0, 46)
        return pref_list[num][0], pref_list[num][1]

    @staticmethod
    def choose_random_yn(pref_list):
        """
        都道府県リストからランダムに１つ選ぶ。標準入力で確認をとる場合。
        基本使わない方針で
        """
        p_select = False
        num = -1
        while p_select is False:
            # 都道府県の番号をランダムに取得
            num = randint(0, 46)
            print(pref_list[num][0], 'で進めてよろしいですか Y/n')
            ans = stdin.readline().rstrip('\r\n')
            if ans == 'Y':
                p_select = True
        return pref_list[num][0], pref_list[num][1]

    def get_recommended_url(self):
        """
        都道府県トップページからエリアやジャンルによる絞り込みのリンクリストを取得
        """
        pref_html = req.urlopen(self.pref_url).read()
        pref_soup = BeautifulSoup(pref_html, "html.parser")
        link_to_reco_a = pref_soup.select("li.list-sidebar__recommend-item > a")
        reco_list = []
        for a in link_to_reco_a:
            href = a.attrs["href"]
            title = a.string
            # 余分なものをひとつずつ除去
            title = title.replace('\n', '')
            title = title.replace(' ', '')
            title = title.replace('×', 'の')
            title = title.replace('・', '＆')
            reco_list.append((title, href))
        print(reco_list)

        target = choice(reco_list)

        return target[0], target[1]

    def get_ranking_url(self):
        """
        該当ページからランキングへのURLを取得
        :return: String
        """
        target_html = req.urlopen(self.target_url).read()
        target_soup = BeautifulSoup(target_html, "html.parser")
        link_to_rank_a = target_soup.select("li.navi-rstlst__tab--rank > a")
        return link_to_rank_a[0].attrs['href']

    def get_ranking_list(self):
        """
        ランキングにアクセスして最大20の情報を取得。
        順位、店名、URL、レビュー１件
        :return:
        """
        ranking_url = self.get_ranking_url()
        ranking_html = req.urlopen(ranking_url).read()
        ranking_soup = BeautifulSoup(ranking_html, "html.parser")

        self.image_file = self.get_image(ranking_soup)

        ranking_a = ranking_soup.select("div.list-rst__rst-name > a")
        ranking_list = []
        for a in ranking_a:
            rank = a.attrs["data-ranking"]
            name = a.string
            url = a.attrs["href"]
            # レビューの取得
            review = self.get_review(url)
            # 店のデータを同時に加える
            print('rank:', rank, 'name:', name, 'review:', review)
            ranking_list.append({"rank": rank, "name": name, "url": url, "review": review})
        return ranking_list

    @staticmethod
    def get_review(rest_url):
        """
        レビューの短い文を5件ぐらい引っ張ってきて1つだけ返す
        """
        rev_url = rest_url + 'dtlrvwlst/COND-0/smp1/D-like/?lc=0&rvw_part=all'
        rev_html = req.urlopen(rev_url).read()
        rev_soup = BeautifulSoup(rev_html, "html.parser")
        rev_list = rev_soup.select("div.rvw-item__rvw-comment > p")
        rev_sentences = []
        for s in rev_list:
            s = str(s)
            # 余分なものをひとつずつ除去
            s = s.replace('<p>', '')
            s = s.replace('</p>', '')
            s = s.replace('</br>', '')
            s = s.replace('<br/>', '')
            s = s.replace('<br>', '')
            s = s.replace(' ', '')
            s = s.replace('\u3000', '')     # 全角スペース
            s = s.replace('\n', '')
            s = s.replace('\n\r', '')
            if len(s) > 3:
                # 文ならせめて3文字より多いでしょうという適当なやつ
                rev_sentences.append(s)
                if len(rev_sentences) >= 5:
                    # 5件得たら終了
                    break
        # 5件のレビューのうちランダムに1つ選んで返却
        rev_sentence = choice(rev_sentences)
        return rev_sentence

    @staticmethod
    def get_image(ranking_soup):
        """
        記事のイメージ画像を引っ張ってくる
        """
        # 画像のURLを取得
        image_a = ranking_soup.select("p.list-rst__photo-item > a > img")
        img_url_small = image_a[0].attrs["data-original"]
        # img_url_large = img_url_small.replace('150x150_square', '640x640_rect')

        # URLにアクセスして画像を保存
        savename = PATH_TABELOG_SRC + 'small_image.png'
        req.urlretrieve(img_url_small, savename)
        print('イメージ画像保存完了')

        return savename


if __name__ == '__main__':

    Tabe = TabelogSearch()

    print(Tabe.pref_name)
    print(Tabe.pref_url)
    print(Tabe.target_name)
    print(Tabe.target_url)
















