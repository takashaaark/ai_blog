from selenium import webdriver

url = "https://matome.naver.jp/"

# PhantomJSのドライバを得る --- (※1)
browser = webdriver.PhantomJS()
# 暗黙的な待機を最大3秒行う --- (※2)
browser.implicitly_wait(3)
# URLを読み込む --- (※3)
browser.get(url)
# 画面をキャプチャしてファイルに保存 --- (※4)
browser.save_screenshot("naver_top.png")
# ブラウザを終了 --- (※5)
browser.quit()

