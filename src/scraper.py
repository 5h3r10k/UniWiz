import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunparse
import os
from collections import deque

# Define the starting URL and a list of allowed domain strings
start_url = "https://www.cs.rutgers.edu/academics/undergraduate/cs-degrees/b-s-degree"  # Change to your starting URL
allowed_domains = ["https://www.cs.rutgers.edu/academics/undergraduate/cs-degrees/b-s-degree", "https://www.cs.rutgers.edu/academics/undergraduate/course-synopses"]  # Add allowed domain strings here

# Ensure the creation of the 'scraped' directory
if not os.path.exists("scraped"):
    os.mkdir("scraped")

def normalize_url(url):
    """Normalize a URL by removing parameters and fragment identifiers."""
    parsed_url = urlparse(url)
    # Reconstruct the URL without parameters (query) and fragment
    normalized_url = urlunparse(parsed_url._replace(query="", fragment=""))
    return normalized_url

def is_valid_url(url, allowed_domains):
    """Check if the URL is valid and starts with any of the allowed domain strings."""
    return any(url.startswith(domain) for domain in allowed_domains)

def get_abs_url(url, allowed_domains):
    """Convert relative URL to absolute URL based on the first allowed domain string."""
    # Assuming the first domain in the list is the main one for relative URLs
    main_domain = allowed_domains[0]
    if url.startswith("/"):
        return urljoin(main_domain, url)
    return url

def scrape_and_save(url, folder="scraped"):
    """Scrape the page content and save it into a file."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
        
        # Define the filename based on the URL to avoid overwriting
        filename = normalize_url(url).replace("https://", "").replace("http://", "").replace("/", "_").rstrip("_") + ".txt"
        filepath = os.path.join(folder, filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Saved: {url}")
    except Exception as e:
        print(f"Error scraping {url}: {e}")

def crawl(start_url, allowed_domains):
    """Recursively crawl the website starting from the start_url."""
    queue = deque([start_url])
    seen = set([normalize_url(start_url)])

    while queue:
        url = queue.popleft()
        print(f"Crawling: {url}")
        try:
            response = requests.get(url)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            scrape_and_save(url)  # Scrape and save the content of the current page

            for link in soup.find_all("a", href=True):
                abs_url = normalize_url(get_abs_url(link['href'], allowed_domains))
                if is_valid_url(abs_url, allowed_domains) and abs_url not in seen:
                    queue.append(abs_url)
                    seen.add(abs_url)

        except Exception as e:
            print(f"Failed to process {url}: {e}")

crawl(start_url, allowed_domains)