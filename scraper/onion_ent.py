import requests
import csv
from bs4 import BeautifulSoup

no_of_rows = 0

with open('onion_ent.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    fields = ["Link", "Title", "Content"]
    csvwriter.writerow(fields)
        
    for thing in range(0, 251, 20):
        page = thing
        url = "https://www.theonion.com/entertainment/news-in-brief?startIndex=0"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
            'Accept-Encoding': 'deflate',
            'Referer': 'https://www.google.com/'
        }
        response = requests.get(url, headers=headers)

        coverpage = response.content
        soup = BeautifulSoup(coverpage, 'html.parser')
        coverpage_news = soup.find_all('a', class_='sc-1out364-0 hMndXN js_link')

        links = []
        list_links = []
        list_titles = []
        news_contents = []


        for elem in coverpage_news:
            links.append(elem['href'])

        links = list(set(links))
        links = [x for x in links if x.startswith("https://www.theonion.com/")]
        links.remove("https://www.theonion.com/rss")

        for i in range(len(links)):
            link = links[i]
            list_links.append(link)

            article = requests.get(link, headers=headers)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html.parser')
            body = soup_article.find_all('p', class_="sc-77igqf-0 bOfvBY")

            if body:
                body = body[0].get_text()
                news_contents.append(body)

                title = soup_article.find_all('h1', class_="sc-1efpnfq-0 bBLibw")
                title = title[0].get_text()
                list_titles.append(title)
            else:
                list_links.pop()

        rows = []

        no_of_rows += len(news_contents)

        for i in range(len(news_contents)):
            rows.append([list_links[i], list_titles[i], news_contents[i]])

        csvwriter.writerows(rows)

print("Done!")
print(f"Wrote {no_of_rows} rows.")
