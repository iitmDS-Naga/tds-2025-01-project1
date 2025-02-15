import httpx
from bs4 import BeautifulSoup
import json
import csv
import os
from urllib.parse import urljoin
import logging
from typing import List, Dict, Union

def task_extract_data_from_website(
    website_url: str,
    css_selectors: List[str],
    output_file_path: str,
    data_format: str = "json",
    max_depth: int = 1,
    request_headers: Dict = None,
    timeout: int = 30
) -> Dict[str, Union[str, int]]:
    """
    Extract data from a website using provided CSS selectors and save to specified format
    
    Args:
        website_url (str): URL of the website to scrape
        css_selectors (list): List of CSS selectors to target elements
        output_file_path (str): Path where scraped data will be saved
        data_format (str): Format to save data (json or csv)
        max_depth (int): Maximum depth of pages to crawl
        request_headers (dict): Custom headers for the HTTP request
        timeout (int): Request timeout in seconds
    
    Returns:
        dict: Status of the operation including number of elements found
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Initialize default headers if none provided
    request_headers = request_headers or {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        scraped_data = []
        visited_urls = set()

        # Using httpx client with context manager
        with httpx.Client(headers=request_headers, timeout=timeout) as client:
            def scrape_page(url: str, depth: int):
                if depth > max_depth or url in visited_urls:
                    return
                
                visited_urls.add(url)
                logger.info(f"Scraping URL: {url}")
                
                response = client.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                page_data = {}
                
                for selector in css_selectors:
                    elements = soup.select(selector)
                    page_data[selector] = [elem.text.strip() for elem in elements]
                
                scraped_data.append(page_data)

            # Start scraping from the initial URL
            scrape_page(website_url, 1)

        # Save the scraped data
        if data_format.lower() == 'json':
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(scraped_data, f, indent=2)
        else:  # csv format
            with open(output_file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write headers
                writer.writerow(css_selectors)
                # Write data
                writer.writerows(scraped_data)
        
        return {
            'status': 'success',
            'elements_found': len(scraped_data),
            'output_file': output_file_path
        }
        
    except httpx.RequestError as e:
        return {
            'status': 'error',
            'message': f'Failed to fetch website: {str(e)}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error during scraping: {str(e)}'
        }