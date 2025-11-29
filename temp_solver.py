import requests
from bs4 import BeautifulSoup

# Basic setup
base_url = "http://example.com"  # Replace with the base URL of the current page you are on
relative_url = "/demo-scrape-data?email=23f2003757@ds.study.iitm.ac.in"
full_url = base_url + relative_url

# Request the page
response = requests.get(full_url)

# Check if the request was successful
if response.status_code == 200:
    data = response.content
    # Since we're expecting a secret code, let's assume it's in JSON format
    try:
        data_json = response.json()
        secret_code = data_json.get('secret', 'Secret code not found')
        print('Secret Code:', secret_code)
        final_answer = secret_code
    except ValueError:
        # If the response is HTML, we'll need to parse it
        soup = BeautifulSoup(data, 'html.parser')
        # Example of how to find a secret code in a div if it's in HTML
        secret_code_tag = soup.find('div', id='secret-code')
        if secret_code_tag:
            secret_code = secret_code_tag.get_text(strip=True)
            print('Secret Code:', secret_code)
            final_answer = secret_code
        else:
            print('Secret code not found in HTML')
            final_answer = None
else:
    print(f'Failed to retrieve data, status code: {response.status_code}')
    final_answer = None

# final_answer now contains the secret code for further steps
