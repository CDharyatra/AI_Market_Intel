#!/usr/bin/env python3
"""
Dataset Merging Script
Merges Kaggle Android and RapidAPI iOS datasets with name matching.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from rapidfuzz import fuzz, process
import os

def load_datasets():
    """Load both Android and iOS datasets."""
    print("Loading datasets...")
    
    # Load Android data
    android_path = "data/processed/kaggle_cleaned.parquet"
    if not Path(android_path).exists():
        raise FileNotFoundError(f"Android dataset not found: {android_path}")
    
    df_android = pd.read_parquet(android_path)
    print(f"Loaded {len(df_android)} Android apps")
    
    # Load iOS data
    ios_path = "data/processed/rapidapi_ios.parquet"
    if not Path(ios_path).exists():
        raise FileNotFoundError(f"iOS dataset not found: {ios_path}")
    
    df_ios = pd.read_parquet(ios_path)
    print(f"Loaded {len(df_ios)} iOS apps")
    
    return df_android, df_ios

def find_name_matches(df_android, df_ios, threshold=80):
    """Find potential matches between Android and iOS apps by name."""
    print(f"Finding name matches with threshold {threshold}%...")
    
    matches = []
    android_names = df_android['app_name'].tolist()
    ios_names = df_ios['app_name'].tolist()
    
    for i, android_name in enumerate(android_names):
        # Find best match for this Android app
        best_match = process.extractOne(
            android_name, 
            ios_names, 
            scorer=fuzz.ratio
        )
        
        if best_match and best_match[1] >= threshold:
            ios_idx = ios_names.index(best_match[0])
            matches.append({
                'android_idx': i,
                'ios_idx': ios_idx,
                'android_name': android_name,
                'ios_name': best_match[0],
                'similarity': best_match[1]
            })
    
    print(f"Found {len(matches)} potential matches")
    return matches

def create_combined_dataset(df_android, df_ios, matches):
    """Create combined dataset with matched and unmatched apps."""
    print("Creating combined dataset...")
    
    # Create copies to avoid modifying originals
    df_android_copy = df_android.copy()
    df_ios_copy = df_ios.copy()
    
    # Add unique IDs
    df_android_copy['app_id'] = 'android_' + df_android_copy.index.astype(str)
    df_ios_copy['app_id'] = 'ios_' + df_ios_copy.index.astype(str)
    
    # Initialize combined apps list
    combined_apps = []
    
    # Mark matched apps
    matched_android_indices = set()
    matched_ios_indices = set()
    
    for match in matches:
        android_idx = match['android_idx']
        ios_idx = match['ios_idx']
        
        matched_android_indices.add(android_idx)
        matched_ios_indices.add(ios_idx)
        
        # Create combined record for matched apps
        android_app = df_android_copy.iloc[android_idx].copy()
        ios_app = df_ios_copy.iloc[ios_idx].copy()
        
        # Use Android data as base, supplement with iOS data where missing
        combined_app = android_app.copy()
        combined_app['platform'] = 'Both'
        combined_app['ios_rating'] = ios_app['rating']
        combined_app['ios_reviews'] = ios_app['reviews']
        combined_app['ios_price'] = ios_app['price_usd']
        combined_app['match_similarity'] = match['similarity']
        combined_app['ios_name'] = ios_app['app_name']
        
        # Ensure last_updated is string
        if 'last_updated' in combined_app and pd.notna(combined_app['last_updated']):
            combined_app['last_updated'] = str(combined_app['last_updated'])
        
        combined_apps.append(combined_app)
    
    # Add unmatched Android apps
    for idx, app in df_android_copy.iterrows():
        if idx not in matched_android_indices:
            app_copy = app.copy()
            app_copy['ios_rating'] = np.nan
            app_copy['ios_reviews'] = 0
            app_copy['ios_price'] = np.nan
            app_copy['match_similarity'] = 0
            app_copy['ios_name'] = ''
            # Ensure last_updated is string
            if 'last_updated' in app_copy and pd.notna(app_copy['last_updated']):
                app_copy['last_updated'] = str(app_copy['last_updated'])
            combined_apps.append(app_copy)
    
    # Add unmatched iOS apps
    for idx, app in df_ios_copy.iterrows():
        if idx not in matched_ios_indices:
            app_copy = app.copy()
            app_copy['platform'] = 'iOS'
            app_copy['ios_rating'] = app['rating']
            app_copy['ios_reviews'] = app['reviews']
            app_copy['ios_price'] = app['price_usd']
            app_copy['match_similarity'] = 0
            app_copy['ios_name'] = app['app_name']
            # Ensure last_updated is string
            if 'last_updated' in app_copy and pd.notna(app_copy['last_updated']):
                app_copy['last_updated'] = str(app_copy['last_updated'])
            combined_apps.append(app_copy)
    
    # Create final DataFrame
    df_combined = pd.DataFrame(combined_apps)
    
    print(f"Combined dataset created with {len(df_combined)} apps")
    return df_combined

def save_matches_report(matches, output_path):
    """Save name matches report."""
    if matches:
        df_matches = pd.DataFrame(matches)
        df_matches.to_csv(output_path, index=False)
        print(f"Saved matches report to {output_path}")
    else:
        print("No matches found to save")

def main():
    """Main function to merge datasets."""
    print("Starting dataset merging...")
    
    try:
        # Load datasets
        df_android, df_ios = load_datasets()
        
        # Find name matches
        matches = find_name_matches(df_android, df_ios, threshold=80)
        
        # Create combined dataset
        df_combined = create_combined_dataset(df_android, df_ios, matches)
        
        # Save combined dataset
        output_path = "data/processed/combined_apps.parquet"
        os.makedirs(Path(output_path).parent, exist_ok=True)
        df_combined.to_parquet(output_path, index=False)
        print(f"Saved combined dataset to {output_path}")
        
        # Save matches report
        matches_path = "artifacts/name_matches.csv"
        os.makedirs(Path(matches_path).parent, exist_ok=True)
        save_matches_report(matches, matches_path)
        
        # Print statistics
        print("\nMerging Statistics:")
        print(f"Total apps in combined dataset: {len(df_combined)}")
        print(f"Android-only apps: {(df_combined['platform'] == 'Android').sum()}")
        print(f"iOS-only apps: {(df_combined['platform'] == 'iOS').sum()}")
        print(f"Cross-platform apps: {(df_combined['platform'] == 'Both').sum()}")
        print(f"Name matches found: {len(matches)}")
        
        if matches:
            avg_similarity = np.mean([m['similarity'] for m in matches])
            print(f"Average match similarity: {avg_similarity:.1f}%")
        
        print("Dataset merging completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during merging: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
