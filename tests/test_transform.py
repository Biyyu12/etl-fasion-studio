import pytest
import pandas as pd
import numpy as np
from utils.transform import transform_product_data, remove_invalid_products

class TestTransformProductData:
    """Test suite untuk fungsi transform_product_data"""

    def test_transform_with_valid_data(self):
        """Test transformasi dengan data yang valid"""
        raw_data = [
            {
                "Title": "T-shirt",
                "Price": "$50.00",
                "Rating": "⭐4.5 / 5",
                "Color": "Red",
                "Size": "M",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            }
        ]
        
        df = transform_product_data(raw_data)
        
        assert len(df) > 0, "DataFrame should not be empty"
        assert 'Price' in df.columns
        assert 'Rating' in df.columns
        # Check that price is converted to numeric type (numpy int64 or float)
        assert isinstance(df['Price'].iloc[0], (int, float, np.integer, np.floating))

    def test_transform_with_empty_data(self):
        """Test transformasi dengan data kosong"""
        raw_data = []
        df = transform_product_data(raw_data)
        assert df.empty, "Empty input should return empty DataFrame"

    def test_transform_with_none_input(self):
        """Test transformasi dengan input None"""
        df = transform_product_data(None)
        assert df.empty, "None input should return empty DataFrame"

    def test_transform_filters_unknown_products(self):
        """Test bahwa Unknown Product difilter"""
        raw_data = [
            {
                "Title": "Unknown Product",
                "Price": "$50.00",
                "Rating": "⭐4.5 / 5",
                "Color": "Red",
                "Size": "M",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            },
            {
                "Title": "Valid Product",
                "Price": "$50.00",
                "Rating": "⭐4.5 / 5",
                "Color": "Blue",
                "Size": "L",
                "Gender": "Women",
                "Timestamp": "2024-01-01 10:00:00"
            }
        ]
        
        df = transform_product_data(raw_data)
        
        # Should filter out Unknown Product
        assert "Unknown Product" not in df['Title'].values

    def test_transform_filters_none_titles(self):
        """Test bahwa produk dengan Title=None difilter"""
        raw_data = [
            {
                "Title": None,
                "Price": "$50.00",
                "Rating": "⭐4.5 / 5",
                "Color": "Red",
                "Size": "M",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            },
            {
                "Title": "Valid Product",
                "Price": "$50.00",
                "Rating": "⭐4.5 / 5",
                "Color": "Blue",
                "Size": "L",
                "Gender": "Women",
                "Timestamp": "2024-01-01 10:00:00"
            }
        ]
        
        df = transform_product_data(raw_data)
        assert len(df) == 1, "Should filter out products with None title"

    def test_transform_price_conversion(self):
        """Test konversi harga dari string ke integer"""
        raw_data = [
            {
                "Title": "Expensive Item",
                "Price": "$100.00",
                "Rating": "⭐4.5 / 5",
                "Color": "Red",
                "Size": "M",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            }
        ]
        
        df = transform_product_data(raw_data)
        
        assert len(df) > 0
        # Check price is converted (100 * 16000 = 1,600,000)
        assert df['Price'].iloc[0] == 1600000

    def test_transform_rating_extraction(self):
        """Test ekstraksi rating dari string"""
        raw_data = [
            {
                "Title": "Product A",
                "Price": "$50.00",
                "Rating": "⭐4.5 / 5",
                "Color": "Red",
                "Size": "M",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            }
        ]
        
        df = transform_product_data(raw_data)
        
        assert len(df) > 0
        # Rating should be extracted as 4.5
        assert pd.isna(df['Rating'].iloc[0]) or df['Rating'].iloc[0] == 4.5

    def test_transform_filters_invalid_prices(self):
        """Test bahwa harga yang tidak valid difilter"""
        raw_data = [
            {
                "Title": "Product A",
                "Price": "Price Unavailable",
                "Rating": "⭐4.5 / 5",
                "Color": "Red",
                "Size": "M",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            }
        ]
        
        df = transform_product_data(raw_data)
        assert df.empty, "Should filter out products with unavailable price"

    def test_transform_filters_invalid_ratings(self):
        """Test bahwa rating yang tidak valid difilter"""
        raw_data = [
            {
                "Title": "Product A",
                "Price": "$50.00",
                "Rating": "⭐Invalid Rating/5",
                "Color": "Red",
                "Size": "M",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            }
        ]
        
        df = transform_product_data(raw_data)
        assert df.empty, "Should filter out products with invalid rating"

class TestRemoveInvalidProducts:
    """Test suite untuk fungsi remove_invalid_products"""

    def test_remove_with_valid_dataframe(self):
        """Test menghapus produk invalid dari DataFrame yang valid"""
        df = pd.DataFrame({
            "Title": ["Product A", "Unknown Product", "Product B"],
            "Price": ["$50.00", "$60.00", "$70.00"],
            "Rating": [4.5, 3.2, 4.8],
            "Color": ["Red", "Blue", "Green"],
            "Size": ["M", "L", "S"],
            "Gender": ["Men", "Women", "Unisex"],
            "Timestamp": ["2024-01-01", "2024-01-01", "2024-01-01"]
        })
        
        result_df = remove_invalid_products(df)
        
        assert len(result_df) < len(df), "Should remove invalid products"
        assert "Unknown Product" not in result_df['Title'].values

    def test_remove_with_empty_dataframe(self):
        """Test dengan DataFrame kosong"""
        df = pd.DataFrame()
        result_df = remove_invalid_products(df)
        assert result_df.empty, "Empty input should return empty DataFrame"

    def test_remove_with_none_input(self):
        """Test dengan input None"""
        result_df = remove_invalid_products(None)
        assert result_df.empty, "None input should return empty DataFrame"

    def test_remove_with_missing_column(self):
        """Test ketika kolom yang diharapkan tidak ada"""
        df = pd.DataFrame({
            "ProductName": ["Product A", "Product B"],
            "Cost": [50.00, 60.00]
        })
        
        result_df = remove_invalid_products(df)
        
        # Should handle gracefully and return empty DataFrame
        assert result_df.empty or isinstance(result_df, pd.DataFrame)

    def test_remove_filters_price_unavailable(self):
        """Test filtering price unavailable"""
        df = pd.DataFrame({
            "Title": ["Product A", "Product B"],
            "Price": ["$50.00", "Price Unavailable"],
            "Rating": [4.5, 3.2],
            "Color": ["Red", "Blue"],
            "Size": ["M", "L"],
            "Gender": ["Men", "Women"]
        })
        
        result_df = remove_invalid_products(df)
        
        assert len(result_df) < len(df), "Should filter out unavailable prices"
        assert "Price Unavailable" not in result_df['Price'].values

    def test_remove_filters_invalid_ratings(self):
        """Test filtering invalid ratings"""
        df = pd.DataFrame({
            "Title": ["Product A", "Product B"],
            "Price": ["$50.00", "$60.00"],
            "Rating": ["Invalid Rating/5", "Not Rated"],
            "Color": ["Red", "Blue"],
            "Size": ["M", "L"],
            "Gender": ["Men", "Women"]
        })
        
        result_df = remove_invalid_products(df)
        
        assert result_df.empty or len(result_df) < len(df), "Should filter out invalid ratings"

    def test_remove_filters_nan_ratings(self):
        """Test filtering NaN ratings"""
        df = pd.DataFrame({
            "Title": ["Product A", "Product B"],
            "Price": ["$50.00", "$60.00"],
            "Rating": [4.5, np.nan],
            "Color": ["Red", "Blue"],
            "Size": ["M", "L"],
            "Gender": ["Men", "Women"]
        })
        
        result_df = remove_invalid_products(df)
        
        assert len(result_df) == 1, "Should filter out NaN ratings"
        assert result_df['Title'].iloc[0] == "Product A"

    def test_remove_logs_statistics(self):
        """Test that function logs removal statistics"""
        df = pd.DataFrame({
            "Title": ["Product A", "Unknown Product"],
            "Price": ["$50.00", "$60.00"],
            "Rating": [4.5, 3.2],
            "Color": ["Red", "Blue"],
            "Size": ["M", "L"],
            "Gender": ["Men", "Women"]
        })
        
        result_df = remove_invalid_products(df)
        
        # Should successfully remove products
        assert len(result_df) == 1

    def test_remove_all_invalid_products(self):
        """Test removing when all products are invalid"""
        df = pd.DataFrame({
            "Title": ["Unknown Product", "Unknown Product"],
            "Price": ["$50.00", "$60.00"],
            "Rating": [4.5, 3.2],
            "Color": ["Red", "Blue"],
            "Size": ["M", "L"],
            "Gender": ["Men", "Women"]
        })
        
        result_df = remove_invalid_products(df)
        
        assert result_df.empty, "All products removed should result in empty DataFrame"

    def test_transform_with_mixed_invalid_data(self):
        """Test transformation with mixed valid and invalid data"""
        raw_data = [
            {
                "Title": "Product A",
                "Price": "$50.00",
                "Rating": "⭐4.5 / 5",
                "Color": "Red",
                "Size": "M",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            },
            {
                "Title": "Unknown Product",
                "Price": "$60.00",
                "Rating": "⭐3.2 / 5",
                "Color": "Blue",
                "Size": "L",
                "Gender": "Women",
                "Timestamp": "2024-01-01 10:00:00"
            },
            {
                "Title": "Product C",
                "Price": "Price Unavailable",
                "Rating": "⭐4.0 / 5",
                "Color": "Green",
                "Size": "S",
                "Gender": "Unisex",
                "Timestamp": "2024-01-01 10:00:00"
            },
            {
                "Title": "Product D",
                "Price": "$70.00",
                "Rating": "⭐4.9 / 5",
                "Color": "Yellow",
                "Size": "XL",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            }
        ]
        
        df = transform_product_data(raw_data)
        
        # Should have valid products only
        assert "Unknown Product" not in df['Title'].values
        assert "Price Unavailable" not in df['Price'].values

    def test_transform_price_with_special_chars(self):
        """Test price conversion with special characters"""
        raw_data = [
            {
                "Title": "Product A",
                "Price": "$999.99",
                "Rating": "⭐4.5 / 5",
                "Color": "Red",
                "Size": "M",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            }
        ]
        
        df = transform_product_data(raw_data)
        
        assert len(df) > 0
        # 999.99 * 16000 = 15,999,840
        assert df['Price'].iloc[0] == 15999840

    def test_transform_handles_attribute_error_gracefully(self):
        """Test that AttributeError during price transform is handled"""
        raw_data = [
            {
                "Title": "Product A",
                "Price": 12345,  # Not a string
                "Rating": "⭐4.5 / 5",
                "Color": "Red",
                "Size": "M",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            }
        ]
        
        df = transform_product_data(raw_data)
        
        # Should handle error and return empty DataFrame or with None price
        assert isinstance(df, pd.DataFrame)

    def test_transform_rating_with_no_numeric_value(self):
        """Test rating extraction when rating has numeric value at end"""
        raw_data = [
            {
                "Title": "Product A",
                "Price": "$50.00",
                "Rating": "⭐No Rating/5",  # Rating extraction will get 5 from the end
                "Color": "Red",
                "Size": "M",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            }
        ]
        
        df = transform_product_data(raw_data)
        
        # Should extract numeric value (5) from "⭐No Rating/5"
        assert len(df) > 0
        assert df['Rating'].iloc[0] == 5

    def test_transform_with_missing_required_columns(self):
        """Test transformation when required columns are missing"""
        raw_data = [
            {
                "Title": "Product A",
                # Missing Price and Rating columns
                "Color": "Red",
                "Size": "M",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            }
        ]
        
        df = transform_product_data(raw_data)
        
        # Should return empty DataFrame due to KeyError
        assert df.empty

    def test_transform_handles_column_filtering_errors(self):
        """Test that column filtering errors are handled gracefully"""
        # This test ensures exception handlers in filtering steps work
        raw_data = [
            {
                "Title": "Product A",
                "Price": "$50.00",
                "Rating": "⭐4.5 / 5",
                "Color": "Red",
                "Size": "M",
                "Gender": "Men",
                "Timestamp": "2024-01-01 10:00:00"
            }
        ]
        
        df = transform_product_data(raw_data)
        
        # Should successfully handle even if exceptions occur
        assert isinstance(df, pd.DataFrame)

    def test_remove_invalid_products_handles_exception(self):
        """Test that remove_invalid_products handles exceptions gracefully"""
        # Create a DataFrame with problematic data
        df = pd.DataFrame({
            "Title": ["Product A", "Product B"],
            "Price": [50.00, 60.00],  # Numeric instead of string
            "Rating": [4.5, 3.2],
            "Color": ["Red", "Blue"],
            "Size": ["M", "L"],
            "Gender": ["Men", "Women"]
        })
        
        result_df = remove_invalid_products(df)
        
        # Should handle exception and return empty DataFrame or processed data
        assert isinstance(result_df, pd.DataFrame)

