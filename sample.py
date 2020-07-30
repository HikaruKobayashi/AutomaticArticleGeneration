import datetime

dt_now = datetime.datetime.now()
today = dt_now.strftime('%Y-%m-%d')

permalink = ('coronavirus-news-' + today)
print (permalink)