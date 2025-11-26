import pandas as pd

def remove_invalid_products(df):
    """Menghapus data produk yang tidak valid berdasarkan kriteria tertentu."""
    # Hapus baris dengan Title = 'Unknown Product'
    df = df[df['Title'] != 'Unknown Product']
    
    # Hapus baris dengan Price = 'Price Unavailable' atau None
    df = df[~df['Price'].isin(['Price Unavailable', None])]
    
    # Hapus baris dengan Rating = 'Invalid Rating/5' atau 'Not Rated'
    df = df[~df['Rating'].isin(['Invalid Rating/5', 'Not Rated'])]
    
    # Hapus baris dengan Rating = NaN (nilai yang tidak bisa dikonversi)
    df = df[df['Rating'].notna()]
    
    return df.reset_index(drop=True)

def transform_product_data(raw_data):
    """Mengubah data menjadi DataFrame."""
    df = pd.DataFrame(raw_data)
    
    # STEP 1: Hapus data invalid terlebih dahulu (sebelum transformasi)
    # Hapus baris dengan Title = 'Unknown Product'
    df = df[df['Title'] != 'Unknown Product']
    
    # Hapus baris dengan Price yang tidak valid
    df = df[~df['Price'].isin(['Price Unavailable', None])]
    
    # Hapus baris dengan Rating yang mengandung "Invalid" atau "Not Rated"
    df = df[~df['Rating'].str.contains('Invalid|Not Rated', regex=True, na=False)]
    
    # STEP 2: Transformasi Price (sekarang data sudah valid)
    df['Price'] = (df['Price'].str.replace(r'[^0-9.]', '', regex=True).astype(float) * 16000).astype(int)
    
    # STEP 3: Transformasi Rating
    df['Rating'] = df['Rating'].str.replace('⭐', '').str.strip()
    df['Rating'] = df['Rating'].str.extract(r'([\d.]+)')[0]
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    
    # STEP 4: Hapus baris dengan Rating yang NaN
    df = df[df['Rating'].notna()]
    
    return df.reset_index(drop=True)




    





    

