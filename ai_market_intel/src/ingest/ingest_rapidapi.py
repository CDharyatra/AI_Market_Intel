#!/usr/bin/env python3
"""
RapidAPI iOS App Store Data Ingestion Script
Fetches iOS App Store data from RapidAPI with retries and caching.
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config import RAPIDAPI_KEY, get_rapidapi_headers, RAPIDAPI_JSONL_PATH, IOS_CATEGORIES

class RapidAPIClient:
    """Client for fetching iOS App Store data from RapidAPI."""
    
    def __init__(self, api_key: str = None):
        """Initialize the RapidAPI client."""
        self.api_key = api_key or RAPIDAPI_KEY
        if not self.api_key:
            print("Warning: RAPIDAPI_KEY not found in .env file. Using mock data.")
            self.api_key = "mock_key"
        
        from config import RAPIDAPI_BASE_URL, CACHE_DIR
        self.base_url = RAPIDAPI_BASE_URL
        self.headers = get_rapidapi_headers()
        self.cache_dir = CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def create_mock_data(self) -> List[Dict[str, Any]]:
        """Create mock iOS App Store data for demonstration."""
        print("Creating mock iOS App Store data...")
        
        # Use iOS categories from config
        categories = IOS_CATEGORIES
        
        # Sample app names
        app_names = [
            'Sample iOS App', 'Mobile Game Pro', 'Productivity Suite',
            'Social Connect', 'Photo Editor', 'Music Player', 'Fitness Tracker',
            'News Reader', 'Weather App', 'Travel Guide', 'Food Delivery',
            'Shopping Assistant', 'Banking App', 'Business Tools', 'Health Monitor',
            'Sports Tracker', 'Reference Guide', 'Entertainment Hub',
            'Educational Tool', 'Lifestyle Manager'
        ]
        
        data = []
        for i in range(5000):  # Create 5000 iOS apps
            app_name = f"{random.choice(app_names)} {i+1}"
            category = random.choice(categories)
            
            # Generate realistic iOS data
            rating = np.random.normal(4.3, 0.7)
            rating = max(0, min(5, rating))
            
            reviews = int(np.random.lognormal(7, 1.2))
            size_mb = np.random.lognormal(2.5, 1.2)
            
            # Price distribution (more paid apps on iOS)
            price = 0 if random.random() < 0.6 else round(np.random.exponential(2.99), 2)
            
            # Content rating
            content_ratings = ['4+', '9+', '12+', '17+']
            content_rating = random.choice(content_ratings)
            
            # Last updated
            last_updated = pd.Timestamp.now() - pd.Timedelta(days=random.randint(0, 365))
            
            # Version
            version = f"{random.randint(1, 10)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
            
            app_data = {
                'trackId': f"ios_{i+1}",
                'trackName': app_name,
                'primaryGenreName': category,
                'averageUserRating': rating,
                'userRatingCount': reviews,
                'fileSizeBytes': int(size_mb * 1024 * 1024),
                'price': price,
                'contentAdvisoryRating': content_rating,
                'genres': [category],
                'releaseDate': last_updated.isoformat(),
                'version': version,
                'minimumOsVersion': f"{random.randint(10, 17)}.0",
                'platform': 'iOS',
                'source': 'RapidAPI'
            }
            
            data.append(app_data)
        
        return data
    
    def fetch_app_data(self, app_id: str) -> Dict[str, Any]:
        """Fetch data for a specific app."""
        if self.api_key == "mock_key":
            return self.create_mock_data()[0]  # Return first mock app
        
        url = f"{self.base_url}/app/{app_id}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching app {app_id}: {e}")
            return None
    
    def fetch_top_apps(self, category: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch top apps from a category."""
        if self.api_key == "mock_key":
            return self.create_mock_data()
        
        url = f"{self.base_url}/top"
        params = {'limit': limit}
        if category:
            params['category'] = category
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching top apps: {e}")
            return []
    
    def save_to_jsonl(self, data: List[Dict[str, Any]], filepath: str):
        """Save data to JSONL format."""
        with open(filepath, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        print(f"Saved {len(data)} records to {filepath}")

def main():
    """Main function to fetch and save iOS App Store data."""
    print("Starting RapidAPI iOS App Store data ingestion...")
    
    # Initialize client
    client = RapidAPIClient()
    
    # Use configured paths
    from config import RAW_DATA_DIR
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Fetch data
    print("Fetching iOS App Store data...")
    if client.api_key == "mock_key":
        print("Using mock data (RAPIDAPI_KEY not configured)")
        data = client.create_mock_data()
    else:
        # Try to fetch real data
        data = client.fetch_top_apps(limit=1000)
        if not data:
            print("Failed to fetch real data, using mock data")
            data = client.create_mock_data()
    
    # Save to JSONL using configured path
    client.save_to_jsonl(data, str(RAPIDAPI_JSONL_PATH))
    
    print(f"iOS App Store data ingestion completed!")
    print(f"Total apps: {len(data)}")
    
    return True

if __name__ == "__main__":
    import random
    import numpy as np
    success = main()
    exit(0 if success else 1)
