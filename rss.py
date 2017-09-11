import feedparser
from newspaper import Article


# right
breitbart_url = 'http://feeds.feedburner.com/breitbart'
nationalreview_url = 'http://www.nationalreview.com/rss.xml'
foxnews_url = 'http://feeds.foxnews.com/foxnews/politics'
watimes_url = 'http://www.washingtontimes.com/rss/headlines/news/politics/'
drudge_url = 'http://www.drudgereportfeed.com/'
redstate_url = ''
# left/moderate
wapo_url = 'https://feeds.washingtonpost.com/rss/politics'
npr_url = 'http://www.npr.org/rss/rss.php?id=1014'
huffington_url = 'http://www.huffingtonpost.com/section/politics/feed'
nyt_url = 'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml'
thehill_url = 'http://thehill.com/rss/syndicator/19110'
cnn_url = 'http://rss.cnn.com/rss/cnn_allpolitics.rss'
vox_url = 'http://www.vox.com/rss/index.xml'
reuters_url = 'http://feeds.reuters.com/Reuters/PoliticsNews'

fp = feedparser.parse(breitbart_url)
feed_title = fp['feed']['title']  # 'Breitbart News'
feed_link = fp['feed']['link']  # 'http://www.breitbart.com'
# print titles, url
for entry in fp.entries:
    print(entry.title, entry.link)

a = Article(fp.entries[0].link)
a.download()
a.parse()
