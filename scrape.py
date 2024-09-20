from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urljoin
import os

load_dotenv()

SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

def read_scraped_data(file_path):
    """Read the scraped data from a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    
def scrape_website(website, depth=2):
    print(f"Connecting to Scraping Browser for {website}...")
    
    service = Service(SBR_WEBDRIVER)
    options = ChromeOptions()
    
    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(website)
        print("Navigated! Scraping page content...")
        html = driver.page_source
        
        content = extract_and_clean_content(html)
        subpages = extract_subpage_links(html, website)
        
        result = {
            'url': website,
            'content': content,
            'subpages': {}
        }
        if depth > 1:
            for i in range(4):
                subpage_url = subpages[i]
                print(f"Scraping subpage: {subpage_url}")
                result['subpages'][subpage_url] = scrape_website(subpage_url, depth - 1)

        return result

def extract_and_clean_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        print("Got body content!")
        for script_or_style in body_content(["script", "style"]):
            script_or_style.extract()
        
        cleaned_content = body_content.get_text(separator="\n")
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )
        return cleaned_content
    return ""

def extract_subpage_links(html_content, base_url):
    soup = BeautifulSoup(html_content, "html.parser")
    links = soup.find_all('a', href=True)
    subpages = set()
    
    for link in links:
        href = link['href']
        full_url = urljoin(base_url, href)
        
        # Check if the link is within the same domain
        if full_url.startswith(base_url):
            subpages.add(full_url)
    
    return list(subpages)

def split_dom_content(dom_content, max_length=6500):
    if not isinstance(dom_content, str):
        try:
            dom_content = str(dom_content)
        except Exception as e:
            print(f"Error converting dom_content to string: {e}")
            return []

    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
