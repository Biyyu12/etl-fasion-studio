from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd

def load_to_db(data, db_url):
    """Fungsi untuk menyimpan data ke dalam PostgreSQL."""
    if create_engine is None:
        print("SQLAlchemy is not installed. Skipping database load.")
        return
    
    try:
        engine = create_engine(db_url)
        
        with engine.connect() as con:
            data.to_sql('products', con=con, if_exists='append', index=False)
            print(f"Data berhasil ditambahkan ke database! ({len(data)} baris)")
    except ModuleNotFoundError as e:
        if 'psycopg2' in str(e):
            print(f"Error: psycopg2 tidak terinstall. Install dengan: pip install psycopg2-binary")
        else:
            print(f"Terjadi kesalahan modul: {e}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke database: {e}")

def load_to_csv(data, file_path):
    """Fungsi untuk menyimpan data ke dalam file CSV."""
    try:
        data.to_csv(file_path, index=False)
        print(f"Data berhasil disimpan ke {file_path}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke CSV: {e}")

def load_to_google_sheets(df,spreadsheet_id: str,range_name: str,service_account_file: str = "./google-sheets-api.json"):
    """Simpan DataFrame ke Google Sheets."""
    try:
        # Setup credential
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Convert DataFrame ke list of lists
        values = [df.columns.tolist()] + df.values.tolist()
        body = {'values': values}

        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"Berhasil menambahkan {len(df)} baris ke Google Sheets!")
    except Exception as e:
        print(f"Gagal menyimpan ke Google Sheets: {e}")

