import pytest
from utils import (
    extract_product_data,
    scrape_products,
    transform_product_data,
    remove_invalid_products,
    load_to_csv,
    load_to_db,
    load_to_google_sheets
)

def test_utils_imports():
    """Test that all utils functions are importable from utils module"""
    assert callable(extract_product_data), "extract_product_data should be callable"
    assert callable(scrape_products), "scrape_products should be callable"
    assert callable(transform_product_data), "transform_product_data should be callable"
    assert callable(remove_invalid_products), "remove_invalid_products should be callable"
    assert callable(load_to_csv), "load_to_csv should be callable"
    assert callable(load_to_db), "load_to_db should be callable"
    assert callable(load_to_google_sheets), "load_to_google_sheets should be callable"

def test_extract_product_data_from_utils():
    """Test extract_product_data imported from utils"""
    from bs4 import BeautifulSoup
    
    html = '<div class="product"><h3 class="product-title">Test</h3></div>'
    section = BeautifulSoup(html, "html.parser").div
    result = extract_product_data(section)
    
    assert result is not None

def test_transform_product_data_from_utils():
    """Test transform_product_data imported from utils"""
    raw_data = [{"Title": "Test", "Price": "$50.00", "Rating": "⭐4.5 / 5", 
                 "Color": "Red", "Size": "M", "Gender": "Men", "Timestamp": "2024-01-01"}]
    df = transform_product_data(raw_data)
    
    assert not df.empty

def test_remove_invalid_products_from_utils():
    """Test remove_invalid_products imported from utils"""
    import pandas as pd
    
    df = pd.DataFrame({
        "Title": ["Product A"],
        "Price": ["$50.00"],
        "Rating": [4.5],
        "Color": ["Red"],
        "Size": ["M"],
        "Gender": ["Men"]
    })
    
    result = remove_invalid_products(df)
    assert isinstance(result, pd.DataFrame)

def test_load_to_csv_from_utils(tmp_path):
    """Test load_to_csv imported from utils"""
    import pandas as pd
    
    csv_file = tmp_path / "test.csv"
    df = pd.DataFrame({"Title": ["Test"], "Price": [50]})
    
    load_to_csv(df, str(csv_file))
    assert csv_file.exists()

def test_scrape_products_from_utils():
    """Test scrape_products imported from utils"""
    from unittest.mock import patch, MagicMock
    
    with patch('utils.extract.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = '<html><body></body></html>'
        mock_get.return_value = mock_response
        
        base_url = "https://example.com/page-{}.html"
        products = scrape_products(base_url, start_page=1, max_pages=1, delay=0)
        
        assert isinstance(products, list)

def test_load_to_db_from_utils():
    """Test load_to_db imported from utils"""
    import pandas as pd
    from unittest.mock import patch
    
    df = pd.DataFrame({
        "Title": ["Test"],
        "Price": [50],
        "Rating": [4.5]
    })
    
    with patch('utils.load.create_engine'):
        load_to_db(df, "postgresql://localhost/db")

def test_load_to_google_sheets_from_utils():
    """Test load_to_google_sheets imported from utils"""
    import pandas as pd
    from unittest.mock import patch
    
    df = pd.DataFrame({
        "Title": ["Test"],
        "Price": [50]
    })
    
    with patch('utils.load.Credentials.from_service_account_file'):
        with patch('utils.load.build'):
            load_to_google_sheets(df, "sheet_id", "Sheet1!A1", "./creds.json")

def test_utils_all_export():
    """Test that __all__ contains all expected exports"""
    from utils import __all__
    
    expected_exports = [
        'extract_product_data',
        'scrape_products',
        'transform_product_data',
        'remove_invalid_products',
        'load_to_csv',
        'load_to_db',
        'load_to_google_sheets'
    ]
    
    for export in expected_exports:
        assert export in __all__, f"{export} should be in __all__"

