#!/usr/bin/env python3
"""
Data Cleaning Script for Kaggle Google Play Store Dataset
Cleans and normalizes the dataset for further processing.
"""

import argparse
import pandas as pd
import numpy as np
import re
from pathlib import Path

def clean_installs(installs_str):
    """Convert installs string to integer."""
    if pd.isna(installs_str) or installs_str == 'Free':
        return 0
    
    # Remove commas and extract number
    installs_str = str(installs_str).replace(',', '').replace('+', '')
    
    # Handle different formats
    if 'k' in installs_str.lower():
        return int(float(installs_str.lower().replace('k', '')) * 1000)
    elif 'm' in installs_str.lower():
        return int(float(installs_str.lower().replace('m', '')) * 1000000)
    elif 'b' in installs_str.lower():
        return int(float(installs_str.lower().replace('b', '')) * 1000000000)
    else:
        try:
            return int(float(installs_str))
        except (ValueError, TypeError):
            return 0

def clean_price(price_str):
    """Convert price string to float USD."""
    if pd.isna(price_str) or price_str == '0' or price_str == 'Free':
        return 0.0
    
    # Remove currency symbols and convert to float
    price_str = str(price_str).replace('$', '').replace(',', '')
    try:
        return float(price_str)
    except (ValueError, TypeError):
        return 0.0

def clean_size(size_str):
    """Convert size string to float MB."""
    if pd.isna(size_str) or size_str == 'Varies with device':
        return np.nan
    
    size_str = str(size_str).upper()
    
    # Extract number and unit
    match = re.search(r'([\d.]+)\s*([KMGT]?B?)', size_str)
    if not match:
        return np.nan
    
    number = float(match.group(1))
    unit = match.group(2)
    
    # Convert to MB
    if unit == 'KB' or unit == 'K':
        return number / 1024
    elif unit == 'MB' or unit == 'M' or unit == '':
        return number
    elif unit == 'GB' or unit == 'G':
        return number * 1024
    else:
        return np.nan

def clean_rating(rating_str):
    """Convert rating to float, handling NaN values."""
    try:
        rating = float(rating_str)
        return rating if 0 <= rating <= 5 else np.nan
    except (ValueError, TypeError):
        return np.nan

def clean_reviews(reviews_str):
    """Convert reviews to integer."""
    try:
        return int(float(str(reviews_str).replace(',', '')))
    except (ValueError, TypeError):
        return 0

def clean_data(df):
    """Apply all cleaning functions to the dataframe."""
    print("Starting data cleaning...")
    print(f"Original shape: {df.shape}")
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Clean installs
    print("Cleaning installs...")
    df_clean['installs'] = df_clean['Installs'].apply(clean_installs)
    
    # Clean price
    print("Cleaning price...")
    df_clean['price_usd'] = df_clean['Price'].apply(clean_price)
    
    # Clean size
    print("Cleaning size...")
    df_clean['size_mb'] = df_clean['Size'].apply(clean_size)
    
    # Clean rating
    print("Cleaning rating...")
    df_clean['rating'] = df_clean['Rating'].apply(clean_rating)
    
    # Clean reviews
    print("Cleaning reviews...")
    df_clean['reviews'] = df_clean['Reviews'].apply(clean_reviews)
    
    # Clean category
    print("Cleaning category...")
    df_clean['category'] = df_clean['Category'].str.strip().str.title()
    
    # Clean app name
    print("Cleaning app name...")
    df_clean['app_name'] = df_clean['App'].str.strip()
    
    # Clean content rating
    print("Cleaning content rating...")
    df_clean['content_rating'] = df_clean['Content Rating'].str.strip()
    
    # Clean genres
    print("Cleaning genres...")
    df_clean['genres'] = df_clean['Genres'].str.strip()
    
    # Clean last updated
    print("Cleaning last updated...")
    df_clean['last_updated'] = pd.to_datetime(df_clean['Last Updated'], errors='coerce')
    
    # Clean current version
    print("Cleaning current version...")
    df_clean['current_version'] = df_clean['Current Ver'].str.strip()
    
    # Clean android version
    print("Cleaning android version...")
    df_clean['android_version'] = df_clean['Android Ver'].str.strip()
    
    # Select and rename columns for final output
    columns_mapping = {
        'app_name': 'app_name',
        'category': 'category',
        'rating': 'rating',
        'reviews': 'reviews',
        'size_mb': 'size_mb',
        'installs': 'installs',
        'price_usd': 'price_usd',
        'content_rating': 'content_rating',
        'genres': 'genres',
        'last_updated': 'last_updated',
        'current_version': 'current_version',
        'android_version': 'android_version'
    }
    
    df_final = df_clean[list(columns_mapping.keys())].copy()
    df_final = df_final.rename(columns=columns_mapping)
    
    # Add platform column
    df_final['platform'] = 'Android'
    
    # Add source column
    df_final['source'] = 'Kaggle'
    
    print(f"Cleaned shape: {df_final.shape}")
    print(f"Columns: {list(df_final.columns)}")
    
    return df_final

def main():
    """Main function to run the cleaning process."""
    parser = argparse.ArgumentParser(description='Clean Kaggle Google Play Store dataset')
    parser.add_argument('--input', required=True, help='Input parquet file path')
    parser.add_argument('--output', required=True, help='Output parquet file path')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not Path(args.input).exists():
        print(f"Input file not found: {args.input}")
        return False
    
    try:
        # Load data
        print(f"Loading data from {args.input}...")
        df = pd.read_parquet(args.input)
        print(f"Loaded {len(df)} rows")
        
        # Clean data
        df_clean = clean_data(df)
        
        # Save cleaned data
        print(f"Saving cleaned data to {args.output}...")
        os.makedirs(Path(args.output).parent, exist_ok=True)
        df_clean.to_parquet(args.output, index=False)
        
        print("Data cleaning completed successfully!")
        print(f"Final dataset shape: {df_clean.shape}")
        
        # Print some statistics
        print("\nDataset Statistics:")
        print(f"Total apps: {len(df_clean)}")
        print(f"Categories: {df_clean['category'].nunique()}")
        print(f"Average rating: {df_clean['rating'].mean():.2f}")
        print(f"Total installs: {df_clean['installs'].sum():,}")
        print(f"Paid apps: {(df_clean['price_usd'] > 0).sum()}")
        
        return True
        
    except Exception as e:
        print(f"Error during cleaning: {e}")
        return False

if __name__ == "__main__":
    import os
    success = main()
    exit(0 if success else 1)
