from ScrawlTE.ScrawlTenMinutes import ScrawlData
if __name__ == "__main__":
    url = "https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.json"
    SD = ScrawlData(url_json=url)
    SD.Scrawing()