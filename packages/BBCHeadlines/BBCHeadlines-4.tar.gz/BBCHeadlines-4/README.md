# BBCNews
A python package to get news from BBC.

### Installation

    pip3 install BBCHeadlines

### Usage
Get all top articles of right now:

    from BBCHeadlines import news
    print(news())

Get the top article:

    print(news(limit=1))

Sample response:

    [
        {
            "title":"US election: Trump campaign seeks partial recount in Wisconsin",
            "title_detail":{
                "type":"text/plain",
                "language":"None",
                "base":"http://feeds.bbci.co.uk/news/world/rss.xml",
                "value":"US election: Trump campaign seeks partial recount in Wisconsin"
            },
            "summary":"Two counties will be asked to recount votes as Donald Trump continues to contest the election result.",
            "summary_detail":{
                "type":"text/html",
                "language":"None",
                "base":"http://feeds.bbci.co.uk/news/world/rss.xml",
                "value":"Two counties will be asked to recount votes as Donald Trump continues to contest the election result."
            },
            "links":[
                {
                    "rel":"alternate",
                    "type":"text/html",
                    "href":"https://www.bbc.co.uk/news/world-us-canada-54994212"
                }
            ],
            "link":"https://www.bbc.co.uk/news/world-us-canada-54994212",
            "id":"https://www.bbc.co.uk/news/world-us-canada-54994212",
            "guidislink":False,
            "published":"Wed, 18 Nov 2020 18:40:53 GMT",
            "published_parsed":time.struct_time(tm_year=2020,
            tm_mon=11,
            tm_mday=18,
            tm_hour=18,
            tm_min=40,
            tm_sec=53,
            tm_wday=2,
            tm_yday=323,
            tm_isdst=0)
        }
    ]