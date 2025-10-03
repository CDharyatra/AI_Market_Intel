#!/usr/bin/env python3
"""
Data Normalization Script
Transforms RapidAPI iOS data to unified schema matching Kaggle data.
"""

import json
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config import RAPIDAPI_JSONL_PATH, IOS_CLEANED_PATH, CONTENT_RATING_MAP, PROCESSED_DATA_DIR

def normalize_ios_data(ios_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Normalize iOS App Store data to unified schema."""
    print("Normalizing iOS App Store data...")
    
    normalized_data = []
    
    for app in ios_data:
        try:
            # Extract and normalize data
            app_name = app.get('trackName', 'Unknown App')
            category = app.get('primaryGenreName', 'Unknown')
            rating = app.get('averageUserRating', 0.0)
            reviews = app.get('userRatingCount', 0)
            
            # Convert file size to MB
            file_size_bytes = app.get('fileSizeBytes', 0)
            size_mb = file_size_bytes / (1024 * 1024) if file_size_bytes > 0 else np.nan
            
            # Price handling
            price = app.get('price', 0.0)
            if isinstance(price, (int, float)):
                price_usd = float(price)
            else:
                price_usd = 0.0
            
            # Content rating mapping from config
            content_rating = CONTENT_RATING_MAP.get(app.get('contentAdvisoryRating', ''), 'Everyone')
            
            # Genres
            genres = app.get('genres', [])
            if isinstance(genres, list):
                genres_str = ', '.join(genres)
            else:
                genres_str = str(genres)
            
            # Last updated
            last_updated = app.get('releaseDate', '')
            if last_updated:
                try:
                    last_updated = pd.to_datetime(last_updated).strftime('%B %d, %Y')
                except:
                    last_updated = 'Unknown'
            else:
                last_updated = 'Unknown'
            
            # Version
            current_version = app.get('version', '1.0.0')
            
            # OS version
            min_os = app.get('minimumOsVersion', '10.0')
            android_version = f"iOS {min_os} and up"
            
            # Create normalized record
            normalized_record = {
                'app_name': app_name,
                'category': category,
                'rating': float(rating) if rating else np.nan,
                'reviews': int(reviews) if reviews else 0,
                'size_mb': size_mb,
                'installs': 0,  # iOS doesn't provide install counts
                'price_usd': price_usd,
                'content_rating': content_rating,
                'genres': genres_str,
                'last_updated': last_updated,
                'current_version': current_version,
                'android_version': android_version,
                'platform': 'iOS',
                'source': 'RapidAPI'
            }
            
            normalized_data.append(normalized_record)
            
        except Exception as e:
            print(f"Error normalizing app {app.get('trackName', 'Unknown')}: {e}")
            continue
    
    df = pd.DataFrame(normalized_data)
    print(f"Normalized {len(df)} iOS apps")
    return df

def load_jsonl(filepath: str) -> List[Dict[str, Any]]:
    """Load data from JSONL file."""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data.append(json.loads(line.strip()))
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON line: {e}")
                continue
    return data

def main():
    """Main function to normalize iOS data."""
    print("Starting iOS data normalization...")
    
    # Use configured paths
    input_path = RAPIDAPI_JSONL_PATH
    output_path = IOS_CLEANED_PATH
    
    # Check if input file exists
    if not Path(input_path).exists():
        print(f"Input file not found: {input_path}")
        return False
    
    try:
        # Load JSONL data
        print(f"Loading data from {input_path}...")
        ios_data = load_jsonl(input_path)
        print(f"Loaded {len(ios_data)} iOS apps")
        
        # Normalize data
        df_normalized = normalize_ios_data(ios_data)
        
        # Save normalized data
        print(f"Saving normalized data to {output_path}...")
        PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        df_normalized.to_parquet(output_path, index=False)
        
        print("iOS data normalization completed successfully!")
        print(f"Final dataset shape: {df_normalized.shape}")
        
        # Print statistics
        print("\niOS Dataset Statistics:")
        print(f"Total apps: {len(df_normalized)}")
        print(f"Categories: {df_normalized['category'].nunique()}")
        print(f"Average rating: {df_normalized['rating'].mean():.2f}")
        print(f"Paid apps: {(df_normalized['price_usd'] > 0).sum()}")
        
        return True
        
    except Exception as e:
        print(f"Error during normalization: {e}")
        return False

if __name__ == "__main__":
    import os
    success = main()
    exit(0 if success else 1)
