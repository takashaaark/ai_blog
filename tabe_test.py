from bs4 import BeautifulSoup
import urllib.request as req

url = "https://tabelog.com/ibaraki/C8220/rstLst/?vs=1&sa" \
      "=%E3%81%A4%E3%81%8F%E3%81%B0%E5%B8%82&sk=&lid" \
      "=top_navi1&vac_net=&svd=20170628&svt=1900&svps=2&hfc=1&sw="
res = req.urlopen(url)
soup = BeautifulSoup(res, "html.parser")


"""
バンザイナポリタンのリンク部分の要素
li.list-rst:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)
"""

restaurant_list = soup.select("li > div")
for r in restaurant_list:
    a = r.a
    if a is not None:
        name = a.string
        href = a.attrs["href"]
        print(name, href)

