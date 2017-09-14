from summus import *
from feedparser import parse


# right-wing feeds
BREITBART_FEED = 'http://www.breitbart.com/big-government/feed/'
NATIONALREVIEW_FEED = 'http://www.nationalreview.com/rss.xml'
FOXNEWS_FEED = 'http://feeds.foxnews.com/foxnews/politics'
WATIMES_FEED = 'http://www.washingtontimes.com/rss/headlines/news/politics/'
DRUDGE_FEED = 'http://www.drudgereportfeed.com/'
REDSTATE_FEED = 'http://www.redstate.com/feed/'
# left-wing feeds
WAPO_FEED = 'http://feeds.washingtonpost.com/rss/politics'
HUFFINGTON_FEED = 'http://www.huffingtonpost.com/section/politics/feed'
THEHILL_FEED = 'http://thehill.com/rss/syndicator/19110'
VOX_FEED = 'http://www.vox.com/rss/index.xml'
NYT_FEED = 'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml'
CNN_FEED = 'http://rss.cnn.com/rss/cnn_allpolitics.rss'
# neutral feeds
NPR_FEED = 'http://www.npr.org/rss/rss.php?id=1014'
REUTERS_FEED = 'http://feeds.reuters.com/Reuters/PoliticsNews'

FEED_LIST = [BREITBART_FEED, FOXNEWS_FEED, DRUDGE_FEED, NYT_FEED, WAPO_FEED, HUFFINGTON_FEED, NPR_FEED, REUTERS_FEED]


class MrManager:
    def __init__(self):
        pass

    def add_feed(self, feed_url):
        fp = parse(feed_url)
        feed = fp['feed']
        entries = fp['entries']
        if not feed or not entries:
            return
        return


class FeedManager:
    def __init__(self, feed_url):
        self.title = ''
        self.language = ''
        self.parse_feed(feed_url)

    def parse_feed(self, feed_url):
        # run parser
        fp = parse(feed_url)
        # check if OK
        feed = fp['feed']
        entries = fp['entries']
        if not feed or not entries:
            return
        # get feed info
        self.title = feed['title']
        self.language = feed['language']


class ArticleManager:
    def __init__(self):
        pass
