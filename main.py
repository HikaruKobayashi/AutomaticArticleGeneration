# coding=utf-8 文字コード
import json
import requests
import schedule
import time
from urllib.parse import urljoin
from datetime import datetime
import settings
import requests
import urllib
from bs4 import BeautifulSoup

# スクレイピング
url = 'https://news.google.com/search'
keyword = 'COVID-19'
params = {'hl':'ja', 'gl':'JP', 'ceid':'JP:ja', 'q':keyword}
article_no = 1
content = 'コロナウイルスに関するまとめ記事'

# WordPressのデータをsettings.pyから取得する。
WP_URL = settings.WP_URL
WP_USERNAME = settings.WP_USERNAME
WP_PASSWORD = settings.WP_PASSWORD
# .envにデータが入っているか確認する。
# print(settings.WP_URL)
# print(settings.WP_USERNAME)
# print(settings.WP_PASSWORD)

def post_article(status, slug, title, content, category_ids, tag_ids, media_id):
  """
  記事を投稿して成功した場合はTrue、失敗した場合はFalseを返します。
  :param status: 記事の状態（公開:publish, 下書き:draft）
  :param slug: 記事識別子。URLの一部になる（ex. slug=aaa-bbb/ccc -> https://wordpress-example.com/aaa-bbb/ccc）
  :param title: 記事のタイトル
  :param content: 記事の本文
  :param category_ids: 記事に付与するカテゴリIDのリスト
  :param tag_ids: 記事に付与するタグIDのリスト
  :param media_id: 見出し画像のID
  :return: レスポンス
  """
  user_ = WP_USERNAME
  pass_ = WP_PASSWORD
  # build request body
  payload = {"status": status,
              "slug": slug,
              "title": title,
              "content": content,
              "date": datetime.now().isoformat(),
              "categories": category_ids,
              "tags": tag_ids}
  if media_id is not None:
    payload['featured_media'] = media_id # アイキャッチ画像
  # send POST request
  res = requests.post(urljoin(WP_URL, "wp-json/wp/v2/posts"),
                    data=json.dumps(payload),
                    headers={'Content-type': "application/json"},
                    auth=(user_, pass_))
  # print('----------\n件名:「{}」の投稿リクエスト結果:{} res.status: {}'.format(title, result, repr(res.status_code)))
  print("Sucess!")
  return res

# スクレイピング対象のURLにリクエスト
res = requests.get(url, params=params)
soup = BeautifulSoup(res.content, "html.parser")

# レスポンスからh3階層のニュースを1件抽出する。
h3_blocks = soup.select(".xrnccd")

for i, h3_entry in enumerate(h3_blocks):
  # 記事を10件取得する。
  if article_no == 11:
    break

  # リンク先URLを取得し、整形してフルパスの<a>タグを作る。
  link = h3_entry.select_one("h3 a")["href"]
  link = urllib.parse.urljoin(url, link)
  # 投稿内容
  # content = '<h2>コロナウイルスに関するまとめ記事</h2>\n<p>おはようございます。本日もコロナウイルスに関するニュースを5記事まとめました。</p>\n<p><a href="' + h3_link + '">' + h3_link + '</a></p>\n<p>本日も「油断大敵」です。元気にいってらっしゃい。</p>\n'
  content = content + '<p><a href="' + link + '">' + link + '</a></p>\n'
  article_no = article_no + 1

  # h3階層のニュースからh4階層のニュースを抽出する
  h4_block = h3_entry.select_one(".SbNwzf")

  if h4_block != None:
    # h4階層が存在するときのみニュースを抽出する
    h4_articles = h4_block.select("article")

    for j, h4_entry in enumerate(h4_articles):
      link = h4_entry.select_one("h4 a")["href"]
      link = urllib.parse.urljoin(URL, link)

      content = content + '<p><a href="' + link + '">' + link + '</a></p>\n'
      article_no = article_no + 1

# 記事を下書き投稿する。（'draft'ではなく、'publish'にすれば公開投稿できます。）
post_article('draft', 'WordPress-New-Post', '【油断大敵】本日のCOVID-19について最新記事まとめ', content, category_ids=[6], tag_ids=[], media_id=575)

# 定期実行
# schedule.every(1).minutes.do(job) # 1分ごとに処理を実装する。

# while True:
#   schedule.run_pending()
#   time.sleep(1)