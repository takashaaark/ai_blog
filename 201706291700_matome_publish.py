"""
NAVERまとめにログインして記事を投稿する。
画像認証がある
"""

from selenium import webdriver
import time
from random import uniform
from sys import stdin

# ユーザー名とパスワードの指定
USER = "takatkjesh4@gmail.com"
PASS = "artificialaffiliate"
URL = 'https://matome.naver.jp/'

# 記事の内容
TITLE = '宮島口で食べるもの'
LINK = ['https://tabelog.com/hiroshima/A3402/A340202/34000098/',
        'https://tabelog.com/hiroshima/A3402/A340202/34011196/',
        'https://tabelog.com/hiroshima/A3402/A340202/34017137/'
        ]


class Capture(object):
    def __init__(self):
        self.png_id = 0

    def capture(self, text):
        # PNG capture
        time.sleep(uniform(2, 5))
        browser.save_screenshot(str(self.png_id) + "_" + text + ".png")
        print(text)
        self.png_id += 1


if __name__ == "__main__":

    PNG = Capture()

    # PhantomJSのドライバーを得る
    browser = webdriver.PhantomJS()
    browser.implicitly_wait(3)

    # url_login = 'https://account.matome.naver.jp/service/login?fromUrl=https%3A%2F%2Fmatome.naver.jp%2F'
    # トップページにアクセス
    browser.get(URL)

    PNG.capture('トップページにアクセスしました')

    # ログインをクリック
    browser.find_element_by_partial_link_text('ログイン').click()

    PNG.capture("ログインページにアクセスしました")

    # テキストボックスに文字を入力
    e = browser.find_element_by_id("_email")
    e.clear()
    e.send_keys(USER)
    e = browser.find_element_by_id("_passwd")
    e.clear()
    e.send_keys(PASS)

    PNG.capture("ログイン情報を入力しました")

    # フォームを送信
    frm = browser.find_element_by_css_selector("#_naver_login_form")
    frm.submit()

    PNG.capture("情報を入力してログインボタンを押しました")

    # まとめ作成をクリック
    browser.find_element_by_partial_link_text('まとめ作成').click()

    PNG.capture("まとめ作成をクリックしました")

    # タイトルの入力
    e = browser.find_element_by_name("title")
    e.clear()
    e.send_keys(TITLE)

    PNG.capture("タイトル「" + TITLE + "」を入力しました")

    # リンクの記述

    for link in LINK:
        # リンクをクリック
        browser.find_element_by_partial_link_text('リンク').click()

        PNG.capture("リンクをクリックしました")

        # リンクの入力
        e = browser.find_element_by_name("url")
        e.clear()
        e.send_keys(link)

        PNG.capture("リンク「" + link + "」を入力しました")

        # チェックをクリック
        browser.find_element_by_class_name('mdBtn01Check01Btn').click()

        PNG.capture("チェックをクリックしました")

        # 保存をクリック
        browser.find_element_by_class_name('mdBtn01Save02Btn').click()

        PNG.capture("保存をクリックしました")

    # 公開をクリック
    browser.find_element_by_class_name('mdBtn01Publish01Btn').click()

    PNG.capture("公開をクリックしました")

    # OKをクリック
    browser.find_element_by_class_name('mdBtn02OK01Btn').click()

    PNG.capture("OKをクリックしました")

    PNG.capture('画像を見て慎重に番号を入力してください')

    number = stdin.readline()

    # 画像認証
    e = browser.find_element_by_class_name('mdInputTxt01InputBox')
    e.clear()
    e.send_keys(number)

    PNG.capture(number + "を入力しました")

    # 公開をクリック
    browser.find_element_by_class_name('mdBtn02Publish01Btn').click()

    PNG.capture("公開をクリックしました")

    # OKをクリック
    browser.find_element_by_class_name('mdBtn02OK01Btn').click()

    PNG.capture("OKをクリックしました")

    PNG.capture("ブラウザを閉じます")

    browser.quit()

