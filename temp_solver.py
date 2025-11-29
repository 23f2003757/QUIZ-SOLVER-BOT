
import requests
from bs4 import BeautifulSoup

# Base URL and endpoint
base_url = "https://tds-llm-analysis.s-anand.net"
data_endpoint = "/demo-scrape-data?email=23f2003757@ds.study.iitm.ac.in"

# Construct full URL
url = base_url + data_endpoint

# Make a GET request to retrieve the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    html_content = response.text
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Assuming that the secret code is located within a specific HTML tag
    # For example, if it's in a div with id="secret-code"
    secret_code_div = soup.find('div', id='secret-code')
    if secret_code_div:
        secret_code = secret_code_div.get_text(strip=True)
    else:
        # If the specific structure is unknown, assuming the secret code might
        # just be the page's text
        secret_code = soup.get_text(strip=True)
    
    # Print the final secret code
    final_answer = {
        "email": "23f2003757@ds.study.iitm.ac.in",
        "secret": secret_code,
        "url": "https://tds-llm-analysis.s-anand.net/demo-scrape?email=23f2003757%40ds.study.iitm.ac.in&id=44097",
        "answer": secret_code
    }
    print(final_answer)
else:
    print("Failed to retrieve the page.")