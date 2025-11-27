import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def remove_invalid_products(df):
    """Menghapus data produk yang tidak valid berdasarkan kriteria tertentu."""
    try:
        if df is None or df.empty:
            logger.warning("Input DataFrame is None or empty. Returning empty DataFrame.")
            return pd.DataFrame()
        
        initial_count = len(df)
        
        # Hapus baris dengan Title = 'Unknown Product'
        df = df[df['Title'] != 'Unknown Product']
        
        # Hapus baris dengan Price = 'Price Unavailable' atau None
        df = df[~df['Price'].isin(['Price Unavailable', None])]
        
        # Hapus baris dengan Rating = 'Invalid Rating/5' atau 'Not Rated'
        df = df[~df['Rating'].isin(['Invalid Rating/5', 'Not Rated'])]
        
        # Hapus baris dengan Rating = NaN (nilai yang tidak bisa dikonversi)
        df = df[df['Rating'].notna()]
        
        removed_count = initial_count - len(df)
        logger.info(f"Removed {removed_count} invalid products. Remaining: {len(df)}")
        
        return df.reset_index(drop=True)
    
    except KeyError as e:
        logger.error(f"Column not found in DataFrame: {e}. Make sure all required columns exist.")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error removing invalid products: {e}")
        return pd.DataFrame()

def transform_product_data(raw_data):
    """Mengubah data menjadi DataFrame dengan error handling."""
    try:
        if not raw_data:
            logger.warning("raw_data is empty. Returning empty DataFrame.")
            return pd.DataFrame()
        
        df = pd.DataFrame(raw_data)
        
        # Filter out None values from extraction
        df = df[df.apply(lambda row: row['Title'] is not None, axis=1)]
        
        logger.info(f"DataFrame created with {len(df)} products.")
        logger.debug(f"DataFrame structure:\n{df.head()}")

        # STEP 1: Hapus data invalid terlebih dahulu (sebelum transformasi)
        # Hapus baris dengan Title = 'Unknown Product'
        try:
            df = df[df['Title'] != 'Unknown Product']
        except Exception as e:
            logger.warning(f"Error filtering 'Unknown Product': {e}")

        # Hapus baris dengan Price yang tidak valid
        try:
            df = df[~df['Price'].isin(['Price Unavailable', None])]
        except Exception as e:
            logger.warning(f"Error filtering invalid prices: {e}")

        # Hapus baris dengan Rating yang mengandung "Invalid" atau "Not Rated"
        try:
            df = df[~df['Rating'].str.contains('Invalid|Not Rated', regex=True, na=False)]
        except Exception as e:
            logger.warning(f"Error filtering invalid ratings: {e}")

        # STEP 2: Transformasi Price (sekarang data sudah valid)
        try:
            df['Price'] = (df['Price'].str.replace(r'[^0-9.]', '', regex=True).astype(float) * 16000).astype(int)
        except Exception as e:
            logger.error(f"Error transforming Price column: {e}")
            df['Price'] = None
        
        # STEP 3: Transformasi Rating
        try:
            df['Rating'] = df['Rating'].str.replace('⭐', '').str.strip()
            df['Rating'] = df['Rating'].str.extract(r'([\d.]+)')[0]
            df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        except Exception as e:
            logger.error(f"Error transforming Rating column: {e}")
            df['Rating'] = None
        
        # STEP 4: Hapus baris dengan Rating yang NaN
        try:
            df = df[df['Rating'].notna()]
        except Exception as e:
            logger.warning(f"Error removing NaN ratings: {e}")
        
        logger.info(f"Transformation complete. Final count: {len(df)} products")
        return df.reset_index(drop=True)
    
    except ValueError as e:
        logger.error(f"ValueError during data transformation: {e}")
        return pd.DataFrame()
    except KeyError as e:
        logger.error(f"Column not found during transformation: {e}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Unexpected error during transformation: {e}")
        return pd.DataFrame()












