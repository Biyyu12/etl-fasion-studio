"""
Utils module for ETL pipeline
Contains functions for Extract, Transform, and Load operations
"""

try:
    from .extract import extract_product_data, scrape_products
except ImportError as e:
    print(f"Warning: Could not import extract module: {e}")

try:
    from .transform import transform_product_data, remove_invalid_products
except ImportError as e:
    print(f"Warning: Could not import transform module: {e}")

try:
    from .load import load_to_csv, load_to_db, load_to_google_sheets
except ImportError as e:
    print(f"Warning: Could not import load module: {e}")

__all__ = [
    'extract_product_data',
    'scrape_products',
    'transform_product_data',
    'remove_invalid_products',
    'load_to_csv',
    'load_to_db',
    'load_to_google_sheets'
]
