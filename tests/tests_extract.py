import pytest
from bs4 import BeautifulSoup
from utils.extract import extract_product_data

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

    assert result['Title'] == "Stylish Shirt"
    assert result['Price'] == "$29.99"  
    assert result['Rating'] == "⭐4.5 out of 5"
    assert result['Color'] == "3"
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

    assert result['Title'] == "Casual Pants"
    assert result['Price'] == "$49.99"
    assert result['Rating'] is None  
    assert result['Color'] == "2"
    assert result['Size'] is None  
    assert result['Gender'] is None  
    assert 'Timestamp' in result