import os
import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from pdfminer.high_level import extract_text
from serpapi import GoogleSearch

# Create directories
BASE_DIR = "scraped_data"
SUB_DIRS = ["docs", "metadata", "pdfs", "text"]
for sub in SUB_DIRS:
    os.makedirs(os.path.join(BASE_DIR, sub), exist_ok=True)

# Get search result URLs from SerpAPI
SERPAPI_KEY = "793075ca93a60b4680f41f667514ef17481a1feb206fe30d631e34870c81be97"
TOPICS = ["Agriculture in India", "Crop rates in India", "Management of crops in India"]
SEARCH_URLS = []

def get_search_urls():
    urls = []
    for topic in TOPICS:
        params = {
            "q": topic,
            "hl": "en",
            "gl": "in",
            "api_key": SERPAPI_KEY
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        if "organic_results" in results:
            urls.extend([res["link"] for res in results["organic_results"]])
    return urls

SEARCH_URLS = get_search_urls()
HEADERS = {'User-Agent': 'Mozilla/5.0'}

class WebScraper(scrapy.Spider):
    name = "web_scraper"
    start_urls = SEARCH_URLS
    
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        title = response.xpath('//title/text()').get() or "Untitled"
        
        # Save text content
        filename = os.path.join(BASE_DIR, "text", f"{title[:50]}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        
        # Save metadata
        metadata_file = os.path.join(BASE_DIR, "metadata", "metadata.txt")
        with open(metadata_file, "a", encoding="utf-8") as f:
            f.write(f"Title: {title}\nURL: {response.url}\n\n")
        
        # Extract PDF links and download
        for link in soup.find_all("a", href=True):
            if link["href"].endswith(".pdf"):
                self.download_pdf(link["href"])
    
    def download_pdf(self, url):
        pdf_path = os.path.join(BASE_DIR, "pdfs", url.split("/")[-1])
        try:
            response = requests.get(url, headers=HEADERS)
            with open(pdf_path, "wb") as f:
                f.write(response.content)
            
            # Extract and save text from PDF
            extracted_text = extract_text(pdf_path)
            text_filename = pdf_path.replace("pdfs", "text").replace(".pdf", ".txt")
            with open(text_filename, "w", encoding="utf-8") as f:
                f.write(extracted_text)
        except Exception as e:
            print(f"Error downloading PDF {url}: {e}")

# Run Scrapy process
process = CrawlerProcess({"USER_AGENT": "Mozilla/5.0"})
process.crawl(WebScraper)
process.start()