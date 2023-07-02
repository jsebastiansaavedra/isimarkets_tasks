
import requests
import os
import re
import json
from bs4 import BeautifulSoup

# Function to scrape and save the articles
def scrape_articles(url, section):

    # Create directory for section if it doesn't exist
    if not os.path.exists(section):
        os.makedirs(section)

    # Make a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the article elements on the page
    articles = list(soup.find_all('article'))


    # Process each article
    for article in articles:
        # Get the article url
        pattern = r'news([^"]+)"'
        match = re.search(pattern, str(article))
        article_url = "https://www.bbc.com/news"+str(match.group(1))

        # Get the content from that url
        response_article = requests.get(article_url)
        print(article_url)
        # Parse the HTML content using BeautifulSoup
        soup_article = BeautifulSoup(response_article.content, 'html.parser')

        # Get the title
        title = soup_article.find('h1').text.strip()

        # Clean the title from bad characters
        invalid_chars = r'[\/:*?"<>|]'
        # Replace them
        title = re.sub(invalid_chars, '', title)


        # Check if the article has already been downloaded
        file_path = f"{section}/{title}.json"
        if os.path.exists(file_path):
            print(f"Skipping '{title}' (already downloaded)")
            continue

        # Get the content
        body_elements = soup_article.findAll('p')
        body = ""
        for content in body_elements:
            body = body + content.get_text()

        # Create a dictionary with the article data
        article_data = {
            'title': title,
            'body': body
        }

        # Save the article as a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(article_data, json_file, indent=4)

        print(f"Downloaded '{title}'")

# URLs of the sections to scrape
sections = {
    'Business': 'https://www.bbc.com/news/business',
    'Tech': 'https://www.bbc.com/news/technology'
}

# Scrape articles from each section
for section, url in sections.items():
    scrape_articles(url, section)
