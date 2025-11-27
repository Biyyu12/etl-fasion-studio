import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def extract_product_data(section):
    """Ekstrak product data denagn beautifulsoup section."""
    try:
        title_elem = section.find("h3", class_="product-title")
        title = title_elem.get_text(strip=True) if title_elem else None
        
        price_elem = section.find("span", class_="price")
        price = price_elem.get_text(strip=True) if price_elem else None

        details = section.find_all("p")

        rating = color = size = gender = None
        for detail in details:
            text = detail.get_text(strip=True)
            if "Rating:" in text:
                rating = text.split("Rating:")[1].strip()
            elif "Colors" in text:
                color = text.split()[0]
            elif "Size:" in text:
                size = text.split("Size:")[1].strip()
            elif "Gender:" in text:
                gender = text.split("Gender:")[1].strip()  
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Color": color,
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp
        }
    except AttributeError as e:
        print(f"Error extracting product data - AttributeError: {e}. Skipping product.")
        return None
    except Exception as e:
        print(f"Unexpected error while extracting product data: {e}. Skipping product.")
        return None

def scrape_products(base_url, start_page=1, max_pages=50, delay=2):
    """Scrape product data from multiple pages with error handling."""
    products = []
    for page in range(start_page, start_page + max_pages):
        url = base_url.format(page)
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code != 200:
                print(f"Failed to retrieve page {page}: Status code {response.status_code}")
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            product_sections = soup.find_all("div", class_="product-details")

            if not product_sections:
                print(f"No products found on page {page}. Continuing to the next page.")
                continue

            for section in product_sections:
                product_data = extract_product_data(section)
                if product_data:  # Only append if extraction was successful
                    products.append(product_data)

            print(f"Scraped page {page} with {len(product_sections)} products.")
            time.sleep(delay)
            
        except requests.exceptions.Timeout:
            print(f"Timeout error while retrieving page {page}. Skipping to next page.")
            continue
        except requests.exceptions.ConnectionError:
            print(f"Connection error while retrieving page {page}. Skipping to next page.")
            continue
        except Exception as e:
            print(f"Unexpected error while scraping page {page}: {e}. Skipping to next page.")
            continue

    if not products:
        print("No products were scraped. Please check the base URL or website structure.")

    return products