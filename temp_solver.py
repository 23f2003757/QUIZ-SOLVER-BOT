

url_to_scrape = 'http://example.com/demo-scrape-data?email=23f2003757@ds.study.iitm.ac.in'

# We will make a GET request to this URL and parse the response
import requests
from bs4 import BeautifulSoup

# Fetch the page
response = requests.get(url_to_scrape)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Assuming the secret code is within some identifiable tag, replace 'your_tag' and 'your_attribute' accordingly
    # Here we assume it's within a <div> with a class 'secret-code', for example
    secret_code_tag = soup.find('div', class_='secret-code')

    # We are assuming the secret code is the text of this tag
    if secret_code_tag:
        secret_code = secret_code_tag.get_text(strip=True)
        final_answer = secret_code
        print(final_answer)
    else:
        print('Secret code not found in the page.')
else:
    print(f'Failed to retrieve the page, status code: {response.status_code}')

