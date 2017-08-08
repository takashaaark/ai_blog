"""
食べログから情報をいただく

"""

import urllib.request as req
from bs4 import BeautifulSoup
from random import randint

URL = 'https://tabelog.com/'


class TabelogSearch(object):
    def __init__(self):
        # 都道府県の番号をランダム出力
        self.num = randint(0, 46)
        # 都道府県リスト
        self.pref_list = self.get_prefecture_list()
        # ランキング上位20
        self.rank_list = self.get_ranking_list()
        # ランキング上位20(URLのみ)
        self.rank_list_url = self.get_ranking_list_url()

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

    def get_ranking_url(self):
        """
        都道府県トップページからランキングのURLを取得
        :return: String
        """
        pref_url = self.pref_list[self.num][1]
        pref_html = req.urlopen(pref_url).read()
        pref_soup = BeautifulSoup(pref_html, "html.parser")
        link_to_rank_a = pref_soup.select("li.navi-rstlst__tab--rank > a")
        return link_to_rank_a[0].attrs['href']

    def get_ranking_list(self):
        """
        ランキングにアクセスして上位20の情報を取得。
        順位、店名、URL
        :return:
        """
        ranking_url = self.get_ranking_url()
        ranking_html = req.urlopen(ranking_url).read()
        ranking_soup = BeautifulSoup(ranking_html, "html.parser")
        ranking_a = ranking_soup.select("div.list-rst__rst-name > a")
        ranking_list = []
        for a in ranking_a:
            rank = a.attrs["data-ranking"]
            title = a.string
            url = a.attrs["href"]
            ranking_list.append((rank, title, url))
        return ranking_list

    def get_ranking_list_url(self):
        url_list = []
        for restaurant in self.rank_list:
            url_list.append(restaurant[2])
        return url_list


if __name__ == '__main__':

    Tabe = TabelogSearch()

    print('都道府県リスト', Tabe.pref_list)

    print('都道府県名とURL:', Tabe.pref_list[Tabe.num])

    print('ランキング結果:', Tabe.rank_list)

    print('ランキング結果(URL)のみ', Tabe.rank_list_url)















