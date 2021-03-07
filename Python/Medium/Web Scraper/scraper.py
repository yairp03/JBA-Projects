import requests
from bs4 import BeautifulSoup
import string
import os


def main():
    pages_amount = int(input())
    article_type = input()
    for page in range(1, pages_amount + 1):
        base_dir = f"Page_{page}"
        os.mkdir(base_dir)
        url = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={page}"
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        soup = BeautifulSoup(response.content, 'html.parser')
        for article in soup.find_all("article"):
            if article.find("span", {"data-test": "article.type"}).text.strip() == article_type:
                title = article.find("a", {"data-track-action": "view article"})
                title_name = title.text
                article_url = "https://www.nature.com" + title.get("href")
                r = requests.get(article_url)
                article_soup = BeautifulSoup(r.content, 'html.parser')
                try:
                    article_body = article_soup.find("div", {"class": "article-item__body"}).text.strip()
                except AttributeError:
                    try:
                        article_body = article_soup.find("div", {"class": "article__body"}).text.strip()
                    except AttributeError:
                        continue
                file_name = os.path.join(base_dir, title_name.translate(str.maketrans(" ", "_", string.punctuation.replace(" ", ""))) + ".txt")
                with open(file_name, "wb") as f:
                    f.write(article_body.encode())
    print('Saved all articles.')


if __name__ == '__main__':
    main()
