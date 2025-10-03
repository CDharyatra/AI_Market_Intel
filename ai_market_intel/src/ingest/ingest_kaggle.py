#!/usr/bin/env python3
"""
Kaggle Dataset Ingestion Script
Downloads and converts Google Play Store apps dataset from Kaggle to parquet format.
"""

import os
import sys
import pandas as pd
import kagglehub
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config import KAGGLE_CSV_PATH, KAGGLE_PARQUET_PATH, RAW_DATA_DIR, FALLBACK_ENCODINGS

def download_kaggle_dataset():
    """Load the real Google Play Store apps dataset from local files."""
    print("Loading real Kaggle dataset from local files...")
    
    # Ensure raw data directory exists
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        # Check if the real dataset exists
        csv_path = KAGGLE_CSV_PATH
        if not os.path.exists(csv_path):
            print("Real dataset not found, falling back to synthetic data...")
            return False
        
        # Load the real dataset
        print("Loading real Google Play Store dataset...")
        df = pd.read_csv(csv_path)
        
        print(f"Real dataset loaded successfully! Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Sample apps: {df['App'].head().tolist()}")
        
        return True
        
    except Exception as e:
        print(f"Error loading real dataset: {e}")
        print("Falling back to synthetic data...")
        return False

def convert_to_parquet():
    """Convert the downloaded CSV to parquet format."""
    csv_path = KAGGLE_CSV_PATH
    parquet_path = KAGGLE_PARQUET_PATH
    
    if not os.path.exists(csv_path):
        print(f"CSV file not found at {csv_path}")
        return False
    
    try:
        print("Converting CSV to parquet...")
        # Try different encodings to handle the real dataset
        df = None
        
        for encoding in FALLBACK_ENCODINGS:
            try:
                df = pd.read_csv(csv_path, encoding=encoding)
                print(f"Successfully loaded with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            print("Could not load CSV with any encoding, using error handling")
            df = pd.read_csv(csv_path, encoding='utf-8', errors='replace')
        
        print(f"Loaded {len(df)} rows from CSV")
        
        # Save as parquet
        df.to_parquet(parquet_path, index=False)
        print(f"Saved parquet file to {parquet_path}")
        
        # Verify the file
        df_check = pd.read_parquet(parquet_path)
        print(f"Verification: {len(df_check)} rows in parquet file")
        
        return True
    except Exception as e:
        print(f"Error converting to parquet: {e}")
        return False

def main():
    """Main function to orchestrate the download and conversion."""
    print("Starting Kaggle dataset ingestion...")
    
    # Check if parquet file already exists
    parquet_path = KAGGLE_PARQUET_PATH
    if os.path.exists(parquet_path):
        print(f"Parquet file already exists at {parquet_path}")
        df = pd.read_parquet(parquet_path)
        print(f"File contains {len(df)} rows")
        return True
    
    # Try to download real dataset first
    if download_kaggle_dataset():
        # Convert to parquet
        if convert_to_parquet():
            print("Real Kaggle dataset ingestion completed successfully!")
            return True
    
    # Fallback to synthetic data if real download fails
    print("Real dataset download failed, creating synthetic data...")
    from create_sample_data import create_sample_dataset
    df = create_sample_dataset()
    
    # Save synthetic data
    csv_path = KAGGLE_CSV_PATH
    df.to_csv(csv_path, index=False)
    print(f"Saved synthetic dataset to {csv_path}")
    
    # Convert to parquet
    if convert_to_parquet():
        print("Synthetic dataset ingestion completed successfully!")
        return True
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
