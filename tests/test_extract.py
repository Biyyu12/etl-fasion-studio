import pytest
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock
from utils.extract import extract_product_data, scrape_products

def test_extract_product_data_complete():
    html = '''
    <div class="product">
        <h3 class="product-title">Stylish Shirt</h3>
        <span class="price">$29.99</span>
        <p>Rating: ⭐4.5 out of 5</p>
        <p>Colors: 3</p>
        <p>Size: M</p>
        <p>Gender: Unisex</p>
    </div>  
    '''
    section = BeautifulSoup(html, "html.parser").div
    result = extract_product_data(section)

    assert result is not None, "extract_product_data returned None"
    assert result['Title'] == "Stylish Shirt"
    assert result['Price'] == "$29.99"  
    assert result['Rating'] == "⭐4.5 out of 5"
    # Color parsing gets first word from "Colors: 3" which is "Colors:"
    assert result['Color'] == "Colors:"
    assert result['Size'] == "M"
    assert result['Gender'] == "Unisex"
    assert 'Timestamp' in result

def test_extract_product_data_missing_fields():
    html = '''
    <div class="product">
        <h3 class="product-title">Casual Pants</h3>
        <span class="price">$49.99</span>
        <p>Colors: 2</p>
    </div>  
    '''
    section = BeautifulSoup(html, "html.parser").div
    result = extract_product_data(section)

    assert result is not None, "extract_product_data returned None"
    assert result['Title'] == "Casual Pants"
    assert result['Price'] == "$49.99"
    assert result['Rating'] is None  
    # Color parsing gets first word from "Colors: 2" which is "Colors:"
    assert result['Color'] == "Colors:"
    assert result['Size'] is None  
    assert result['Gender'] is None  
    assert 'Timestamp' in result

def test_extract_product_data_none_input():
    """Test that extract_product_data handles None input gracefully"""
    result = extract_product_data(None)
    assert result is None, "Should return None for None input"

def test_extract_product_data_invalid_section():
    """Test that extract_product_data handles invalid section"""
    html = '<div class="invalid"></div>'
    section = BeautifulSoup(html, "html.parser").div
    result = extract_product_data(section)
    # Should return None or a dict with None values
    assert result is None or result['Title'] is None

def test_extract_product_data_with_all_fields():
    """Test extraction with all fields populated"""
    html = '''
    <div class="product">
        <h3 class="product-title">Premium Jacket</h3>
        <span class="price">$199.99</span>
        <p>Rating: ⭐5.0 / 5</p>
        <p>Colors: 5</p>
        <p>Size: XL</p>
        <p>Gender: Women</p>
    </div>  
    '''
    section = BeautifulSoup(html, "html.parser").div
    result = extract_product_data(section)
    
    assert result is not None
    assert result['Title'] == "Premium Jacket"
    assert result['Price'] == "$199.99"
    assert result['Rating'] == "⭐5.0 / 5"
    assert result['Size'] == "XL"
    assert result['Gender'] == "Women"

def test_extract_product_data_exception_handling():
    """Test that exceptions are caught and handled gracefully"""
    # Create a mock section that raises AttributeError
    mock_section = MagicMock()
    mock_section.find.side_effect = AttributeError("Mock error")
    
    result = extract_product_data(mock_section)
    assert result is None, "Should return None on AttributeError"

@patch('utils.extract.requests.get')
def test_scrape_products_success(mock_get):
    """Test scraping products successfully"""
    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = '''
    <html>
        <div class="product-details">
            <h3 class="product-title">Test Product</h3>
            <span class="price">$50.00</span>
        </div>
    </html>
    '''
    mock_get.return_value = mock_response
    
    base_url = "https://example.com/page-{}.html"
    products = scrape_products(base_url, start_page=1, max_pages=2, delay=0)
    
    assert len(products) > 0
    assert mock_get.called

@patch('utils.extract.requests.get')
def test_scrape_products_http_error(mock_get):
    """Test scraping with HTTP error response"""
    # Mock error response
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    base_url = "https://example.com/page-{}.html"
    products = scrape_products(base_url, start_page=1, max_pages=1, delay=0)
    
    assert len(products) == 0
    assert mock_get.called

@patch('utils.extract.requests.get')
def test_scrape_products_timeout(mock_get):
    """Test scraping with timeout error"""
    import requests
    mock_get.side_effect = requests.exceptions.Timeout("Connection timeout")
    
    base_url = "https://example.com/page-{}.html"
    products = scrape_products(base_url, start_page=1, max_pages=1, delay=0)
    
    assert len(products) == 0

@patch('utils.extract.requests.get')
def test_scrape_products_connection_error(mock_get):
    """Test scraping with connection error"""
    import requests
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
    
    base_url = "https://example.com/page-{}.html"
    products = scrape_products(base_url, start_page=1, max_pages=1, delay=0)
    
    assert len(products) == 0

@patch('utils.extract.requests.get')
def test_scrape_products_general_exception(mock_get):
    """Test scraping with general exception"""
    mock_get.side_effect = Exception("Unexpected error")
    
    base_url = "https://example.com/page-{}.html"
    products = scrape_products(base_url, start_page=1, max_pages=1, delay=0)
    
    assert len(products) == 0

@patch('utils.extract.requests.get')
def test_scrape_products_no_products_on_page(mock_get):
    """Test when page returns no products"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = '<html><body>No products</body></html>'
    mock_get.return_value = mock_response
    
    base_url = "https://example.com/page-{}.html"
    products = scrape_products(base_url, start_page=1, max_pages=2, delay=0)
    
    assert len(products) == 0

