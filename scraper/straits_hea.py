import requests
import csv
from bs4 import BeautifulSoup

no_of_rows = 0

with open('straits_hea.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    fields = ["Link", "Title", "Content"]
    csvwriter.writerow(fields)
        
    for thing in range(11):
        page = thing
        url = f"https://www.straitstimes.com/singapore/health?page={page}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
            'Accept-Encoding': 'deflate',
            'Referer': 'https://www.google.com/'
        }
        response = requests.get(url, headers=headers)

        coverpage = response.content
        soup = BeautifulSoup(coverpage, 'html5lib')
        coverpage_news = soup.find_all('a', class_='stretched-link')
        coverpage_titles = soup.find_all('h5', class_='card-title')

        list_links = []
        list_titles = []
        news_contents = []

        for i in range(len(coverpage_news)):
            link = f"https://www.straitstimes.com{coverpage_news[i]['href']}" 
            list_links.append(link)

            title = coverpage_titles[i].find_all('a')[0].contents[0]
            list_titles.append(title)

            article = requests.get(link, headers=headers)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html5lib')
            body = soup_article.find_all('div', class_='article-content-rawhtml')

            if body:
                body = body[0].find_all('div', class_='field--name-field-paragraph-text')

                list_paragraphs = []
                for x in body:
                    text = x.find_all('p')
                    for p in text:
                        paragraph = p.get_text()
                        list_paragraphs.append(paragraph)
                    final_article = " ".join(list_paragraphs)

                news_contents.append(final_article)
            else:
                list_links.pop()
                list_titles.pop()

        rows = []

        no_of_rows += len(news_contents)

        for i in range(len(news_contents)):
            rows.append([list_links[i], list_titles[i], news_contents[i]])

        csvwriter.writerows(rows)

print("Done!")
print(f"Wrote {no_of_rows} rows.")
