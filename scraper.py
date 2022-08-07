import urllib.request
import bs4 as bs

class ContentScraper:
    """
    Used to parse the HTML of a url to extract data from certain tags"
    """

    def __init__(self, url):
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        scraped_data = urllib.request.urlopen(req)
        article = scraped_data.read()
        parsed_article = bs.BeautifulSoup(article, 'lxml')
        paragraphs = parsed_article.find_all('p')
        self.article_text = ""

        for p in paragraphs:
            article_text += "\n"
            self.article_text += p.text
        
        print(article_text, "\n\n")

ContentScraper(url="https://www.straitstimes.com/world/europe/who-could-be-part-of-a-us-russia-prisoner-exchange")