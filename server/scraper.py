import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import json

def is_valid_url(url, base_url):
    """ Check if a URL is valid and belongs to the same domain as the base URL """
    parsed_url = urlparse(url)
    parsed_base = urlparse(base_url)
    return bool(parsed_url.netloc) and parsed_url.netloc == parsed_base.netloc

def clean_text(soup):
    """ Remove script and style elements and return clean text """
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()  # Remove these elements
    return soup.get_text(separator=' ', strip=True)

def scrape_url(url, base_url, visited_urls, data):
    """ Recursively scrape data from the given URL """
    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Store the page title and cleaned content in the data dictionary
        page_title = soup.title.string if soup.title else 'No Title'
        cleaned_text = clean_text(soup)
        data[page_title] = cleaned_text

        # Find and process all links on the page
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            if is_valid_url(full_url, base_url):
                scrape_url(full_url, base_url, visited_urls, data)
    except requests.RequestException as e:
        print(f"Request failed: {e}")

# Starting URL
base_url = 'https://admissions.umd.edu/'
visited_urls = set()
data = {}

scrape_url(base_url, base_url, visited_urls, data)

# Write the data to a JSON file
with open('scraped_content.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# Get the size of the file
file_size = os.path.getsize('scraped_content.json')
print(f"The size of the file is: {file_size} bytes")
