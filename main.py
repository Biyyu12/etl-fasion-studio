from utils.extract import extract_product_data, scrape_products
from utils.transform import transform_product_data, remove_invalid_products
from utils.load import load_to_csv, load_to_db, load_to_google_sheets

def main():
    BASE_URL = "https://fashion-studio.dicoding.dev/?page={}"
    START_PAGE = 1
    MAX_PAGES = 50
    DELAY = 5  

    print("=== Starting ETL Pipeline ===")

    # Step 1: Scrape product data
    print("========================================")
    print("Step 1: Extracting data from website...")
    print("========================================")    
    raw_products = scrape_products(BASE_URL, START_PAGE, MAX_PAGES, DELAY)
    
    # Step 2: Transform the data
    print("========================================")
    print("Step 2: Transforming and cleaning data...")
    print("========================================")
    transformed_data = transform_product_data(raw_products)
    cleaned_data = remove_invalid_products(transformed_data)
    print(f"Total valid products after cleaning: {len(cleaned_data)}")

    # Step 3: Load the data
    print("========================================")
    print("Step 3: Loading data to destinations...")
    print("========================================")
    CSV_FILE_PATH = "products.csv"
    DB_URL = "postgresql+psycopg2://developer:Abiyyu#121204@localhost:5432/productdb"

    load_to_csv(cleaned_data, CSV_FILE_PATH)
    load_to_db(cleaned_data, DB_URL)
    SPREADSHEET_ID = "1r43LCsyoSDnoZUAFl9cVXz3dFpAccycYBO4MVAR5-1g"
    RANGE_NAME = "Sheet1!A1"
    load_to_google_sheets(cleaned_data, SPREADSHEET_ID, RANGE_NAME)


if __name__ == "__main__":
    main()

