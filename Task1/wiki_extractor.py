import requests as req
import wikipedia
from bs4 import BeautifulSoup
import re
import json
import argparse


'''-------------------1. WIKI FETCH-------------------------------------'''

def wiki_fetch(keyword, num_urls):
    return wikipedia.search(keyword, results=num_urls)


'''-------------------2. SCRAPPING DATA---------------------------------'''

def prepare_data(results):
    json_content = []
    i = 0
    for link in results:
        i += 1
        url = "https://en.wikipedia.org/wiki/"+link

        response = req.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = ''
        for para in soup.find_all("p"):
            text += para.text
        text = re.sub(r"\[.*?\]+", '', text)
        # To remove non ascii characters
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        text = text.replace('\n', ' ')
        text = text.split('.')
        text = ''.join(text[:10])
        json_content.append({"url": url, "paragraph": text})
    return json_content


'''-------------------3. PREPARING JSON FILE----------------------------'''

def save_json_file(filepath, json_content):
    with open(filepath, "w") as file:
        json.dump(json_content, file, indent=2, ensure_ascii=False)


'''------------------------MAIN FUNCTION--------------------------------'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", help="Enter query that you want to search", type=str)
    parser.add_argument("--num_urls", help="Number of pages to search for", type=int)
    parser.add_argument("--output", help="Name of output json file", type=str)
    args = parser.parse_args()

    results = wiki_fetch(keyword=args.keyword, num_urls=args.num_urls)
    json_content = prepare_data(results=results)
    save_json_file(filepath=args.output, json_content=json_content)


if __name__ == "__main__":
    main()
