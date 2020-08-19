# coding=utf-8 文字コード
import json
import requests
import datetime
import time
from urllib.parse import urljoin
import settings
import requests
import urllib
from bs4 import BeautifulSoup

# タイトル
title = '【油断大敵】本日のCOVID-19について最新記事まとめ'

# パーマリンクを作成する為に日付を取得する。
dt_now = datetime.datetime.now()
today = dt_now.strftime('%Y-%m-%d')
# パーマリンク作成
permalink = ('coronavirus-news-' + today)

# スクレイピング
url = 'https://news.google.com/search'
keyword = 'COVID-19'
params = {'hl':'ja', 'gl':'JP', 'ceid':'JP:ja', 'q':keyword}
article_no = 1
content = '<h2>コロナウイルスに関する記事5選</h2>\n<p>おはようございます。本日もコロナウイルスに関するニュースを5つピックアップしました。</p>'
conclusion = '<p>いかかでしたでしょうか。少しでもご自分の健康を守るための参考になればと思います。</p>\n<p>今日も「油断大敵」を忘れずに元気に過ごしてください。</p>'

# WordPressのデータをsettings.pyから取得する。
WP_URL = settings.WP_URL
WP_USERNAME = settings.WP_USERNAME
WP_PASSWORD = settings.WP_PASSWORD

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
              "date": datetime.datetime.now().isoformat(),
              "categories": category_ids,
              "tags": tag_ids}
  if media_id is not None:
    payload['featured_media'] = media_id # アイキャッチ画像
  # send POST request
  res = requests.post(urljoin(WP_URL, "wp-json/wp/v2/posts"),
                    data=json.dumps(payload),
                    headers={'Content-type': "application/json"},
                    auth=(user_, pass_))
  print("Sucess!")
  return res

# スクレイピング対象のURLにリクエスト
res = requests.get(url, params=params)
soup = BeautifulSoup(res.content, "html.parser")

# レスポンスからh3階層のニュースを1件抽出する。
h3_blocks = soup.select(".xrnccd")

for i, h3_entry in enumerate(h3_blocks):
  # 記事を5件取得する。
  if article_no == 6:
    break

  # リンク先URLを取得し、整形してフルパスの<a>タグを作る。
  link = h3_entry.select_one("h3 a")["href"]
  link = urllib.parse.urljoin(url, link)
  # 投稿内容
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

# 記事を投稿する。（'draft':下書き、'publish':公開投稿）
post_article('publish', permalink, title, content+conclusion, category_ids=[8], tag_ids=[], media_id=575)