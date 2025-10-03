#!/usr/bin/env python3
"""
Statistical Aggregates Computation Script
Computes statistical aggregates for the combined app dataset.
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
import os

def load_combined_data():
    """Load the combined app dataset."""
    data_path = "data/processed/combined_apps.parquet"
    if not Path(data_path).exists():
        raise FileNotFoundError(f"Combined dataset not found: {data_path}")
    
    df = pd.read_parquet(data_path)
    print(f"Loaded combined dataset with {len(df)} apps")
    return df

def compute_category_stats(df):
    """Compute statistics by category."""
    print("Computing category statistics...")
    
    category_stats = []
    
    for category in df['category'].unique():
        if pd.isna(category):
            continue
            
        cat_data = df[df['category'] == category]
        
        stats = {
            'category': category,
            'total_apps': len(cat_data),
            'android_apps': len(cat_data[cat_data['platform'].isin(['Android', 'Both'])]),
            'ios_apps': len(cat_data[cat_data['platform'].isin(['iOS', 'Both'])]),
            'cross_platform_apps': len(cat_data[cat_data['platform'] == 'Both']),
            'avg_rating': cat_data['rating'].mean(),
            'median_rating': cat_data['rating'].median(),
            'total_reviews': cat_data['reviews'].sum(),
            'avg_reviews': cat_data['reviews'].mean(),
            'total_installs': cat_data['installs'].sum(),
            'avg_installs': cat_data['installs'].mean(),
            'paid_apps': len(cat_data[cat_data['price_usd'] > 0]),
            'free_apps': len(cat_data[cat_data['price_usd'] == 0]),
            'avg_price': cat_data[cat_data['price_usd'] > 0]['price_usd'].mean(),
            'median_price': cat_data[cat_data['price_usd'] > 0]['price_usd'].median(),
            'avg_size_mb': cat_data['size_mb'].mean(),
            'median_size_mb': cat_data['size_mb'].median()
        }
        
        # Handle NaN values
        for key, value in stats.items():
            if pd.isna(value):
                stats[key] = 0
        
        category_stats.append(stats)
    
    return category_stats

def compute_platform_stats(df):
    """Compute statistics by platform."""
    print("Computing platform statistics...")
    
    platform_stats = {}
    
    for platform in ['Android', 'iOS', 'Both']:
        platform_data = df[df['platform'] == platform]
        
        if len(platform_data) == 0:
            continue
            
        stats = {
            'platform': platform,
            'total_apps': len(platform_data),
            'avg_rating': platform_data['rating'].mean(),
            'median_rating': platform_data['rating'].median(),
            'total_reviews': platform_data['reviews'].sum(),
            'avg_reviews': platform_data['reviews'].mean(),
            'total_installs': platform_data['installs'].sum(),
            'avg_installs': platform_data['installs'].mean(),
            'paid_apps': len(platform_data[platform_data['price_usd'] > 0]),
            'free_apps': len(platform_data[platform_data['price_usd'] == 0]),
            'avg_price': platform_data[platform_data['price_usd'] > 0]['price_usd'].mean(),
            'median_price': platform_data[platform_data['price_usd'] > 0]['price_usd'].median(),
            'avg_size_mb': platform_data['size_mb'].mean(),
            'median_size_mb': platform_data['size_mb'].median()
        }
        
        # Handle NaN values
        for key, value in stats.items():
            if pd.isna(value):
                stats[key] = 0
        
        platform_stats[platform] = stats
    
    return platform_stats

def compute_overall_stats(df):
    """Compute overall dataset statistics."""
    print("Computing overall statistics...")
    
    overall_stats = {
        'total_apps': len(df),
        'total_categories': df['category'].nunique(),
        'total_platforms': df['platform'].nunique(),
        'avg_rating': df['rating'].mean(),
        'median_rating': df['rating'].median(),
        'total_reviews': df['reviews'].sum(),
        'total_installs': df['installs'].sum(),
        'paid_apps': len(df[df['price_usd'] > 0]),
        'free_apps': len(df[df['price_usd'] == 0]),
        'avg_price': df[df['price_usd'] > 0]['price_usd'].mean(),
        'median_price': df[df['price_usd'] > 0]['price_usd'].median(),
        'avg_size_mb': df['size_mb'].mean(),
        'median_size_mb': df['size_mb'].median(),
        'top_categories': df['category'].value_counts().head(10).to_dict(),
        'platform_distribution': df['platform'].value_counts().to_dict()
    }
    
    # Handle NaN values
    for key, value in overall_stats.items():
        if pd.isna(value):
            overall_stats[key] = 0
    
    return overall_stats

def compute_cross_platform_insights(df):
    """Compute insights for cross-platform apps."""
    print("Computing cross-platform insights...")
    
    cross_platform = df[df['platform'] == 'Both']
    
    if len(cross_platform) == 0:
        return {}
    
    insights = {
        'total_cross_platform_apps': len(cross_platform),
        'avg_android_rating': cross_platform['rating'].mean(),
        'avg_ios_rating': cross_platform['ios_rating'].mean(),
        'rating_difference': cross_platform['rating'].mean() - cross_platform['ios_rating'].mean(),
        'avg_android_reviews': cross_platform['reviews'].mean(),
        'avg_ios_reviews': cross_platform['ios_reviews'].mean(),
        'price_consistency': len(cross_platform[cross_platform['price_usd'] == cross_platform['ios_price']]),
        'avg_price_difference': (cross_platform['price_usd'] - cross_platform['ios_price']).mean()
    }
    
    # Handle NaN values
    for key, value in insights.items():
        if pd.isna(value):
            insights[key] = 0
    
    return insights

def main():
    """Main function to compute all aggregates."""
    print("Starting statistical aggregates computation...")
    
    try:
        # Load data
        df = load_combined_data()
        
        # Compute statistics
        category_stats = compute_category_stats(df)
        platform_stats = compute_platform_stats(df)
        overall_stats = compute_overall_stats(df)
        cross_platform_insights = compute_cross_platform_insights(df)
        
        # Combine all statistics
        aggregates = {
            'overall_stats': overall_stats,
            'category_stats': category_stats,
            'platform_stats': platform_stats,
            'cross_platform_insights': cross_platform_insights,
            'computation_timestamp': pd.Timestamp.now().isoformat()
        }
        
        # Save aggregates
        output_path = "artifacts/aggregates.json"
        os.makedirs(Path(output_path).parent, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(aggregates, f, indent=2, default=str)
        
        print(f"Saved aggregates to {output_path}")
        
        # Print summary
        print("\nAggregates Summary:")
        print(f"Total apps analyzed: {overall_stats['total_apps']:,}")
        print(f"Categories: {overall_stats['total_categories']}")
        print(f"Average rating: {overall_stats['avg_rating']:.2f}")
        print(f"Paid apps: {overall_stats['paid_apps']:,} ({overall_stats['paid_apps']/overall_stats['total_apps']*100:.1f}%)")
        print(f"Cross-platform apps: {cross_platform_insights.get('total_cross_platform_apps', 0):,}")
        
        print("Statistical aggregates computation completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during computation: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
