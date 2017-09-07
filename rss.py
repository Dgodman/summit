import feedparser


breitbart_url = 'https://feeds.feedburner.com/breitbart'
fp = feedparser.parse(breitbart_url)
feed_title = fp['feed']['title']  # 'Breitbart News'
feed_link = fp['feed']['link']  # 'http://www.breitbart.com'
# print titles, url
for post in fp.entries:
    print(post.title, post.link)
