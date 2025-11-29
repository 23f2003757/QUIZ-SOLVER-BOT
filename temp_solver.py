import requests
from bs4 import BeautifulSoup

# Fetch the page
url = "https://tds-llm-analysis.s-anand.net/demo"
response = requests.get(url)

# Parse the page
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the dynamic content
span_origin = soup.find(class_='origin')

if span_origin:
    final_answer = span_origin.text
else:
    final_answer = "Element not found"

print(final_answer)