from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
from reportlab.pdfgen import canvas
from urllib.request import urlopen
import ssl
from urllib.error import HTTPError


utalist = []
url = 'https://www.uta.edu/admissions'
def get_url(url):
    #specify the url
    try:
        page = urlopen(url, context=ssl._create_unverified_context())
        soup = BeautifulSoup(page, features="html.parser")
        all_links = soup.find_all('a')
        for link in all_links:
            href = link.get('href')
            if href and 'https:' in href and 'uta.edu/admissions' in href:
                # Check if the URL already exists in utalist
                if href not in utalist:
                    utalist.append(href)
                    # Recursively call get_url to navigate through each URL
                    get_url(href)
        utalist.append('https://www.uta.edu/admissions/partnerships/t3/faqs')
    # Process the page content
    except Exception as e:
        print("Error:", e)

def get_txt():
    get_url(url)
    txt_filename = 'recursive_txt.txt'
    with open(txt_filename, 'w', encoding='utf-8') as txt_file:
        for link in utalist:
            list_texts = []
            try:
                page = urlopen(link, context=ssl._create_unverified_context()) 
                soup2 = BeautifulSoup(page, features="html.parser")
                tables = soup2.find_all('table')
                for table in tables:
                    # Extract text from each cell in the table
                    table_text = '\n'.join([cell.get_text(separator=' ', strip=True) for cell in table.find_all(['td', 'th'])])
                    list_texts.append(table_text)
                for x in soup2.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6','p']):
                    list_texts.append(x.get_text())
                
                for text in list_texts:
                        txt_file.write(text + '\n')
            except HTTPError as e:
            # Print an error message if the URL returns a 404 status code
                print(f"Error: {e}")
    print("Text file is formed!!")
    return txt_filename
