# parser/url_parser.py

import requests
from bs4 import BeautifulSoup  # Import BeautifulSoup

from src.extractors.extract_pdf_content import read_pdf_split_by_page


def url_parser(url, title):
    # Get URL data
    response = requests.get(url)

    # Parse pdf
    if response.status_code == 200 and 'application/pdf' in response.headers['Content-Type']:
        pdf_bytes = response.content
        parsed_content = read_pdf_split_by_page(pdf_bytes=pdf_bytes, title=title)

    elif response.status_code == 200 and 'text/html' in response.headers['Content-Type']:
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the title tag and get its text
        page_title = soup.title.string if soup.title else "No Title Found"

        # Update parsed_document to include the webpage's title
        parsed_content = {
            'title': page_title,
            'document_type': "text/html",
            'pages': [{
                'page_number': 1,
                'text': response.text  # Use response.text for UTF-8 encoded text
            }]
        }

    else:
        print(response.status_code)
        print(response.headers['Content-Type'])
        print("Failed to retrieve the PDF or the content is not a PDF.")
        exit()

    return parsed_content
