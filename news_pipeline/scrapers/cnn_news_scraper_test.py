import cnn_news_scraper as scraper

EXPECTED_NEWS = "performing an act of violence against a person at an airport serving international civil aviation that caused"
CNN_NEWS_URL = "http://edition.cnn.com/2017/01/17/us/fort-lauderdale-shooter-isis-claim/index.html"

def test_basic():
    news = scraper.extract_news(CNN_NEWS_URL)

    assert EXPECTED_NEWS in news
    print ("test passed")

if __name__ == "__main__":
    test_basic()