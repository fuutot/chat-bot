from requests_html import HTMLSession

session = HTMLSession()

# サポーターズ利用規約
url = "https://talent.supporterz.jp/terms/"

res = session.get(url)
print(res.text)