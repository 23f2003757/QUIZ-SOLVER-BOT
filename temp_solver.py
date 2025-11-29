import requests
from bs4 import BeautifulSoup

# Base URL and relative path to scrape
demo_scrape_url = 'https://tds-llm-analysis.s-anand.net/demo-scrape-data?email=23f2003757@ds.study.iitm.ac.in'

# Request the page
response = requests.get(demo_scrape_url)

# Parse the content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Assuming the secret code is within a tag with a specific attribute or structure
# Here we assume that secret code is within a specific id/class/element
# As we don't have full HTML content, make assumptions; for real scraping, ensure to inspect the page structure
secret_code = ''

# Look for known patterns, e.g., <span id="secret_code">, etc.
# Since this is assumed, modify as per actual page structure
secret_element = soup.find(id="secret_code")

if secret_element:
    secret_code = secret_element.text.strip()

# If it's a different tag, such as a paragraph with a specific class
if not secret_code:
    secret_element = soup.find('p', class_='secret-class')
    if secret_element:
        secret_code = secret_element.text.strip()

# Print the secret code
print(secret_code)