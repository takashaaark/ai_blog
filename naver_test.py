"""
NAVERまとめでいろいろ試す
"""

from selenium import webdriver

png_id = 0

# PhantomJSのドライバーを得る
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)

# ページにアクセス
url_login = 'https://matome.naver.jp/'
browser.get(url_login)

# PNG capture
browser.save_screenshot(str(png_id)+"naver_top.png")
png_id += 1
print("ページにアクセスしました")

browser.find_element_by_partial_link_text('まとめ作成').click()

# PNG capture
browser.save_screenshot(str(png_id)+"naver_create_matome.png")
png_id += 1
print("まとめ作成にアクセスしました")

browser.find_element_by_partial_link_text('ログアウト').click()


browser.quit()


