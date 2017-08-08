"""
NAVERまとめにログインして記事を投稿する。
画像認証がある
"""

from selenium import webdriver
import time
from random import uniform
from sys import stdin

# ユーザー名とパスワードの指定
EMAIL = "takatkjesh4@gmail.com"
PASS = "artificialaffiliate"
URL = 'https://matome.naver.jp/'


class MatomePublish(object):
    def __init__(self, title, link_list):
        self.email = EMAIL
        self.password = PASS
        self.top_url = URL
        # PhantomJSのドライバーを得る
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(3)
        self.png_id = 0
        self.title = title
        self.link_list = link_list
        # 記事の公開
        self.publish()

    def png_capture(self, text):
        """
        画面のキャプチャー
        :param text:
        :return:
        """
        time.sleep(uniform(3, 7))
        self.browser.save_screenshot("png/" + str(self.png_id) + "_" + text + ".png")
        print(text)
        self.png_id += 1

    def only_message(self, text):
        """
        画面のキャプチャーはいらないという場合
        :param text:
        :return:
        """
        self.browser.implicitly_wait(uniform(2, 5))
        print(text)

    def publish(self):
        # トップページにアクセス
        self.browser.get(self.top_url)
        self.png_capture('トップページにアクセスしました')

        # ログインをクリック
        self.browser.find_element_by_partial_link_text('ログイン').click()
        self.png_capture("ログインページにアクセスしました")

        # メールアドレスの入力
        e = self.browser.find_element_by_id("_email")
        e.clear()
        e.send_keys(self.email)

        # パスワードの入力
        e = self.browser.find_element_by_id("_passwd")
        e.clear()
        e.send_keys(self.password)
        self.png_capture("ログイン情報を入力しました")

        # フォームを送信
        frm = self.browser.find_element_by_css_selector("#_naver_login_form")
        frm.submit()
        self.png_capture("情報を入力してログインボタンを押しました")

        # まとめ作成をクリック
        self.browser.find_element_by_partial_link_text('まとめ作成').click()

        self.png_capture("まとめ作成をクリックしました")

        # タイトルの入力
        e = self.browser.find_element_by_name("title")
        e.clear()
        e.send_keys(self.title)

        self.png_capture("タイトル「" + self.title + "」を入力しました")

        # リンクの記述

        for link in self.link_list:
            # リンクをクリック
            self.browser.find_element_by_partial_link_text('リンク').click()
            self.png_capture("リンクをクリックしました")

            # リンクの入力
            e = self.browser.find_element_by_class_name("mdMTMWidget01FormAdd01UrlInputbox")
            e.clear()
            e.send_keys(link)
            self.png_capture("リンクを入力しました")

            # チェックをクリック
            self.browser.find_element_by_class_name('mdBtn01Check01Btn').click()
            self.png_capture("チェックをクリックしました")

            # 保存をクリック
            self.browser.find_element_by_class_name('mdBtn01Save02Btn').click()
            self.png_capture("保存をクリックしました")

        # 公開をクリック
        self.browser.find_element_by_class_name('mdBtn01Publish01Btn').click()
        self.only_message("公開をクリックしました")

        # OKをクリック
        self.browser.find_element_by_class_name('mdBtn02OK01Btn').click()
        self.only_message("OKをクリックしました")

        self.png_capture('画像を見て慎重に番号を入力してください')

        number = stdin.readline().rstrip('\r\n')

        # 画像認証
        e = self.browser.find_element_by_class_name('mdInputTxt01InputBox')
        e.clear()
        e.send_keys(number)

        self.png_capture(number + "を入力しました")

        # 公開をクリック
        self.browser.find_element_by_class_name('mdBtn02Publish01Btn').click()
        self.png_capture("公開をクリックしました")

        # OKをクリック
        self.browser.find_element_by_class_name('mdBtn02OK01Btn').click()
        self.png_capture("OKをクリックしました")

        self.only_message("ブラウザを閉じます")

        self.browser.quit()


if __name__ == "__main__":
    # 記事の内容
    T = '岡山県で食べるべきものランキング'
    L = ['https://tabelog.com/okayama/A3301/A330104/33000059/',
         'https://tabelog.com/okayama/A3301/A330101/33000111/',
         'https://tabelog.com/okayama/A3301/A330101/33001952/'
            ]

    Matome = MatomePublish(T, L)


