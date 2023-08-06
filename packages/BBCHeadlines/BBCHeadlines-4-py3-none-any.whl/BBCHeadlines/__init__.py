import feedparser

def news(limit=False):
    entries = feedparser.parse('http://feeds.bbci.co.uk/news/world/rss.xml')['entries']
    if limit:
        return(entries[:limit])
    else:
        return(entries)

print(
    len(news()))