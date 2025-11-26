try:
    from sqlalchemy import create_engine
except ImportError:
    create_engine = None

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
except ImportError:
    Credentials = None
    build = None

def load_to_db(data, db_url):
    """Fungsi untuk menyimpan data ke dalam PostgreSQL."""
    if create_engine is None:
        print("SQLAlchemy is not installed. Skipping database load.")
        return
    
    try:
        engine = create_engine(db_url)
        
        with engine.connect() as connection:
            data.to_sql('products', con=connection, if_exists='append', index=False)
            print("Data berhasil ditambahkan!.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke database: {e}")

def load_to_csv(data, file_path):
    """Fungsi untuk menyimpan data ke dalam file CSV."""
    try:
        data.to_csv(file_path, index=False)
        print(f"Data berhasil disimpan ke {file_path}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke CSV: {e}")

def load_to_google_sheets(data, spreadsheet_id, sheet_name, credentials_json):
    """Fungsi untuk menyimpan data ke Google Sheets."""
    if Credentials is None or build is None:
        print("Google API libraries are not installed. Skipping Google Sheets load.")
        return
    
    try:
        creds = Credentials.from_service_account_file(credentials_json, scopes=["https://www.googleapis.com/auth/spreadsheets"])
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        # Convert DataFrame to list of lists
        values = [data.columns.tolist()] + data.values.tolist()
        
        body = {
            'values': values
        }
        
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=sheet_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"{result.get('updatedCells')} cells updated in Google Sheets.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke Google Sheets: {e}")
