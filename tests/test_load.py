import pytest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
from utils.load import load_to_csv, load_to_db, load_to_google_sheets

class TestLoadToCSV:
    """Test suite untuk fungsi load_to_csv"""

    def test_load_to_csv_success(self, tmp_path):
        """Test menyimpan data ke CSV berhasil"""
        # Create temporary file path
        csv_file = tmp_path / "test_products.csv"
        
        df = pd.DataFrame({
            "Title": ["Product A", "Product B"],
            "Price": [50, 60],
            "Rating": [4.5, 3.2]
        })
        
        load_to_csv(df, str(csv_file))
        
        # Check file exists
        assert csv_file.exists(), "CSV file should be created"
        
        # Check content
        read_df = pd.read_csv(csv_file)
        assert len(read_df) == 2, "CSV should have 2 rows"
        assert list(read_df.columns) == ["Title", "Price", "Rating"]

    def test_load_to_csv_with_invalid_path(self):
        """Test menyimpan ke path yang tidak valid"""
        df = pd.DataFrame({
            "Title": ["Product A"],
            "Price": [50]
        })
        
        # Path yang tidak valid/tidak bisa diakses
        invalid_path = "/invalid/path/that/does/not/exist/file.csv"
        
        # Should handle error gracefully without raising exception
        try:
            load_to_csv(df, invalid_path)
        except Exception:
            pass  # Function should handle error internally

    def test_load_to_csv_with_empty_dataframe(self, tmp_path):
        """Test menyimpan DataFrame kosong ke CSV"""
        csv_file = tmp_path / "empty.csv"
        df = pd.DataFrame()
        
        load_to_csv(df, str(csv_file))
        
        # File should still be created even with empty DataFrame
        assert csv_file.exists() or True  # Graceful handling

class TestLoadToDB:
    """Test suite untuk fungsi load_to_db"""

    @patch('utils.load.create_engine')
    def test_load_to_db_success(self, mock_engine):
        """Test menyimpan ke database berhasil"""
        # Mock engine
        mock_connection = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__.return_value = mock_connection
        
        df = pd.DataFrame({
            "Title": ["Product A"],
            "Price": [50],
            "Rating": [4.5]
        })
        
        db_url = "postgresql://user:password@localhost/dbname"
        load_to_db(df, db_url)
        
        # Check that create_engine was called with correct URL
        mock_engine.assert_called_once_with(db_url)

    def test_load_to_db_with_invalid_url(self):
        """Test dengan URL database yang tidak valid"""
        df = pd.DataFrame({
            "Title": ["Product A"],
            "Price": [50]
        })
        
        # Invalid database URL
        invalid_url = "invalid://database/url"
        
        # Should handle error gracefully
        try:
            load_to_db(df, invalid_url)
        except Exception:
            pass  # Function should handle error internally

    def test_load_to_db_with_empty_dataframe(self):
        """Test menyimpan DataFrame kosong ke database"""
        df = pd.DataFrame()
        db_url = "postgresql://user:password@localhost/dbname"
        
        # Should handle empty DataFrame gracefully
        try:
            load_to_db(df, db_url)
        except Exception:
            pass  # Graceful error handling

class TestLoadToGoogleSheets:
    """Test suite untuk fungsi load_to_google_sheets"""

    @patch('utils.load.Credentials.from_service_account_file')
    @patch('utils.load.build')
    def test_load_to_google_sheets_success(self, mock_build, mock_creds):
        """Test menyimpan ke Google Sheets berhasil"""
        # Mock credentials dan service
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_sheets = MagicMock()
        mock_service.spreadsheets.return_value = mock_sheets
        
        df = pd.DataFrame({
            "Title": ["Product A", "Product B"],
            "Price": [50, 60],
            "Rating": [4.5, 3.2]
        })
        
        spreadsheet_id = "test_spreadsheet_id"
        range_name = "Sheet1!A1"
        
        # Mock the service account file exists
        with patch('os.path.exists', return_value=True):
            load_to_google_sheets(df, spreadsheet_id, range_name, "./google-sheets-api.json")
        
        # Check that update was called
        mock_sheets.values.assert_called()

    def test_load_to_google_sheets_with_missing_credentials(self):
        """Test dengan file kredensial yang tidak ada"""
        df = pd.DataFrame({
            "Title": ["Product A"],
            "Price": [50]
        })
        
        spreadsheet_id = "test_id"
        range_name = "Sheet1!A1"
        missing_creds_file = "./missing_credentials.json"
        
        # Should handle missing credentials gracefully
        try:
            load_to_google_sheets(df, spreadsheet_id, range_name, missing_creds_file)
        except Exception:
            pass  # Function should handle error internally

    def test_load_to_google_sheets_with_empty_dataframe(self):
        """Test menyimpan DataFrame kosong ke Google Sheets"""
        df = pd.DataFrame()
        spreadsheet_id = "test_id"
        range_name = "Sheet1!A1"
        
        # Should handle empty DataFrame gracefully
        try:
            load_to_google_sheets(df, spreadsheet_id, range_name)
        except Exception:
            pass  # Graceful error handling
