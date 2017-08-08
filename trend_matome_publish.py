"""
NAVERまとめにログインして記事を投稿する。
画像認証がある
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import time
from datetime import datetime
from random import uniform
from sys import stdin

import subprocess

import twitter_tweet
import twitter_get_reply

from data import *

# ユーザー名とパスワードの指定
EMAIL = "takatkjesh4@gmail.com"
PASS = "artificialaffiliate"
URL = 'https://matome.naver.jp/'

# 要素が現れるまでの最大待ち時間
IMPLICIT_TIME = 1000


class MatomePublish(object):
    def __init__(self, title, img_file, data_list):
        self.email = EMAIL
        self.password = PASS
        self.top_url = URL
        # PhantomJSのドライバーを得る
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(IMPLICIT_TIME)
        self.png_id = 0
        # 引数の取得
        self.title = title
        self.img_file = img_file
        self.data_list = data_list
        # 記事のURL
        self.matome_url = ''
        # 記事の投稿に失敗したらFalse
        self.status = True
        # 記事の公開
        self.publish()

    def png_capture(self, text):
        """
        画面のキャプチャー
        :param text:
        :return:
        """
        time.sleep(uniform(3, 7))
        self.browser.save_screenshot(PATH_TREND_DEBUG + str(self.png_id) + "_" + text + ".png")
        print(text)
        self.png_id += 1

    def png_capture2(self):
        """
        画像認証画面のキャプチャー。
        :param text:
        :return:
        """
        png_time = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        png_address = PATH_NUM_CERTIFY + 'numbers_' + png_time + '.png'

        time.sleep(uniform(3, 7))
        self.browser.save_screenshot(png_address)
        print(png_address + "に画像認証を保存しました")
        self.png_id += 1

        return png_address

    @staticmethod
    def only_message(text):
        """
        画面のキャプチャーはいらないという場合
        :param text:
        :return:
        """
        time.sleep(uniform(3, 7))
        print(text)

    def publish(self):
        try:

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

            # タイトル画像の追加
            self.browser.find_element_by_class_name("mdBtn02Toggle01Txt").click()
            self.png_capture("オプション項目をクリックしました")

            self.browser.find_element_by_class_name("_jUploadImage").click()
            self.png_capture("アップロードをクリックしました")

            e = self.browser.find_element_by_name("Filedata")
            e.send_keys(self.img_file)
            self.png_capture("画像ファイルをアップロードしました")

            self.browser.find_element_by_class_name("btnUpload").click()
            self.png_capture("登録をクリックしました")

            # Twitterの記述
            for data in self.data_list[0:10]:
                # Twitterをクリック
                self.browser.find_element_by_partial_link_text('Twitter').click()
                self.only_message("Twitterをクリックしました")

                # ツイートのURLの入力
                e = self.browser.find_element_by_class_name("mdMTMWidget01FormAdd04UrlInputbox")
                e.clear()
                e.send_keys(data)
                self.only_message("ツイートのURLを入力しました")

                # チェックをクリック
                self.browser.find_element_by_class_name('mdBtn01Check01Btn').click()
                self.only_message("チェックをクリックしました")

                # 保存をクリック
                self.browser.find_element_by_class_name('mdBtn01Save02Btn').click()
                self.png_capture("保存をクリックしました")

            # 公開をクリック
            self.browser.find_element_by_class_name('mdBtn01Publish01Btn').click()
            self.png_capture("公開をクリックしました")

            # OKをクリック
            self.browser.find_element_by_class_name('mdBtn02OK01Btn').click()
            self.png_capture("OKをクリックしました")

            # つぶやいておく
            twitter_tweet.tweet_sentence("そろそろ画像認証が来そうだ")

            # TODO: 認証失敗時はここに戻る

            # 認証画面の保存
            png_address = self.png_capture2()

            # ツイッター経由で解く
            twitter_tweet.send_secure_request(png_address)
            number = twitter_get_reply.get_reply()

            # コマンドライン経由で解く
            # self.png_capture('画像を見て慎重に番号を入力してください')
            # number = stdin.readline().rstrip('\r\n')

            if number is None:
                print('返事が来ないので下書き保存しておきます。')

                # キャンセルをクリック
                self.browser.find_element_by_class_name('mdBtn02Cancel01Btn').click()
                self.png_capture("キャンセルをクリックしました")

                # 下書き保存をクリック
                self.browser.find_element_by_class_name('mdBtn01SaveDraft01Btn').click()
                self.png_capture("下書き保存をクリックしました")

                self.status = False
            else:
                # PNGの名前を変更
                cmd = 'mv ' + png_address + ' ' + png_address.replace('numbers', number)
                print('$', cmd)
                subprocess.call(cmd, shell=True)

                # 画像認証
                e = self.browser.find_element_by_class_name('mdInputTxt01InputBox')
                e.clear()
                e.send_keys(number)

                self.png_capture(number + "を入力しました")

                # 公開をクリック
                self.browser.find_element_by_class_name('mdBtn02Publish01Btn').click()
                self.png_capture("公開をクリックしました")

                # TODO: 認証失敗の対策

                # OKをクリック
                self.browser.find_element_by_class_name('mdBtn02OK01Btn').click()
                self.png_capture("OKをクリックしました")

                self.matome_url = self.browser.current_url

            self.only_message("ブラウザを閉じます")
            self.browser.quit()

        except NoSuchElementException:

            twitter_tweet.tweet_sentence("謎のエラーだ。下書き保存しておこう")

            # 下書き保存をクリック
            self.browser.find_element_by_class_name('mdBtn01SaveDraft01Btn').click()
            self.png_capture("下書き保存をクリックしました")

            self.only_message("ブラウザを閉じます")
            self.browser.quit()

            self.status = False

            return


if __name__ == "__main__":
    pass
