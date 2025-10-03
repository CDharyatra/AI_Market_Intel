#!/usr/bin/env python3
"""
Insights Enrichment Script
Adds statistical confidence scores and generates charts for insights.
"""

import json
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from scipy import stats

def load_insights(filepath):
    """Load insights from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def load_combined_data():
    """Load the combined app dataset for statistical analysis."""
    data_path = "data/processed/combined_apps.parquet"
    if not Path(data_path).exists():
        raise FileNotFoundError(f"Combined dataset not found: {data_path}")
    
    return pd.read_parquet(data_path)

def calculate_confidence_scores(insights, df):
    """Calculate statistical confidence scores for insights."""
    print("Calculating confidence scores...")
    
    enriched_insights = insights.copy()
    
    for insight in enriched_insights['insights']:
        confidence = 0.5  # Base confidence
        
        # Adjust confidence based on data quality and sample size
        if 'supporting_data' in insight:
            supporting_data = insight['supporting_data']
            
            # Sample size confidence
            total_apps = len(df)
            if total_apps > 10000:
                confidence += 0.2
            elif total_apps > 5000:
                confidence += 0.1
            
            # Data completeness confidence
            if 'ios_avg_rating' in supporting_data and 'android_avg_rating' in supporting_data:
                ios_rating = supporting_data['ios_avg_rating']
                android_rating = supporting_data['android_avg_rating']
                
                if ios_rating > 0 and android_rating > 0:
                    # Higher confidence for larger rating differences
                    rating_diff = abs(ios_rating - android_rating)
                    if rating_diff > 0.5:
                        confidence += 0.2
                    elif rating_diff > 0.2:
                        confidence += 0.1
            
            # Statistical significance (simplified)
            if 'cross_platform_count' in supporting_data:
                cross_platform_count = supporting_data['cross_platform_count']
                if cross_platform_count > 1000:
                    confidence += 0.1
                elif cross_platform_count > 500:
                    confidence += 0.05
        
        # Cap confidence at 1.0
        confidence = min(confidence, 1.0)
        insight['confidence'] = round(confidence, 2)
    
    return enriched_insights

def generate_charts(insights, df):
    """Generate charts to support insights."""
    print("Generating supporting charts...")
    
    # Create charts directory
    charts_dir = Path("artifacts/charts")
    charts_dir.mkdir(parents=True, exist_ok=True)
    
    # Set style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # Chart 1: Platform Rating Comparison
    plt.figure(figsize=(10, 6))
    platform_ratings = df.groupby('platform')['rating'].mean().sort_values(ascending=False)
    bars = plt.bar(platform_ratings.index, platform_ratings.values, alpha=0.7)
    plt.title('Average App Ratings by Platform', fontsize=14, fontweight='bold')
    plt.xlabel('Platform', fontsize=12)
    plt.ylabel('Average Rating', fontsize=12)
    plt.ylim(0, 5)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{height:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(charts_dir / 'platform_ratings.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Chart 2: Category Distribution
    plt.figure(figsize=(12, 8))
    category_counts = df['category'].value_counts().head(10)
    bars = plt.barh(range(len(category_counts)), category_counts.values, alpha=0.7)
    plt.yticks(range(len(category_counts)), category_counts.index)
    plt.title('Top 10 App Categories by Count', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Apps', fontsize=12)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + 10, bar.get_y() + bar.get_height()/2,
                f'{int(width)}', ha='left', va='center')
    
    plt.tight_layout()
    plt.savefig(charts_dir / 'category_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Chart 3: Price Distribution
    plt.figure(figsize=(10, 6))
    paid_apps = df[df['price_usd'] > 0]['price_usd']
    if len(paid_apps) > 0:
        plt.hist(paid_apps, bins=50, alpha=0.7, edgecolor='black')
        plt.title('Distribution of Paid App Prices', fontsize=14, fontweight='bold')
        plt.xlabel('Price (USD)', fontsize=12)
        plt.ylabel('Number of Apps', fontsize=12)
        plt.xlim(0, min(50, paid_apps.max()))  # Cap at $50 for better visualization
        plt.tight_layout()
        plt.savefig(charts_dir / 'price_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    # Chart 4: Rating vs Reviews Scatter
    plt.figure(figsize=(10, 6))
    sample_data = df.sample(min(5000, len(df)))  # Sample for performance
    scatter = plt.scatter(sample_data['reviews'], sample_data['rating'], 
                         alpha=0.5, s=20)
    plt.title('App Rating vs Number of Reviews', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Reviews', fontsize=12)
    plt.ylabel('Rating', fontsize=12)
    plt.xscale('log')
    plt.tight_layout()
    plt.savefig(charts_dir / 'rating_vs_reviews.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Chart 5: Platform Market Share
    plt.figure(figsize=(8, 8))
    platform_counts = df['platform'].value_counts()
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    wedges, texts, autotexts = plt.pie(platform_counts.values, 
                                      labels=platform_counts.index,
                                      autopct='%1.1f%%',
                                      colors=colors,
                                      startangle=90)
    plt.title('App Distribution by Platform', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(charts_dir / 'platform_share.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Generated {len(list(charts_dir.glob('*.png')))} charts in {charts_dir}")
    
    # Add chart references to insights
    chart_files = [f.name for f in charts_dir.glob('*.png')]
    return chart_files

def add_chart_references(insights, chart_files):
    """Add chart references to insights."""
    chart_mapping = {
        'platform_ratings.png': 'Platform rating comparison',
        'category_distribution.png': 'Category distribution',
        'price_distribution.png': 'Price distribution',
        'rating_vs_reviews.png': 'Rating vs reviews correlation',
        'platform_share.png': 'Platform market share'
    }
    
    for insight in insights['insights']:
        if 'charts' not in insight:
            insight['charts'] = []
        
        # Add relevant charts based on insight category
        if insight['category'] == 'Platform Comparison':
            insight['charts'].extend(['platform_ratings.png', 'platform_share.png'])
        elif insight['category'] == 'Market Analysis':
            insight['charts'].extend(['category_distribution.png'])
        elif insight['category'] == 'Monetization':
            insight['charts'].extend(['price_distribution.png'])
        elif insight['category'] == 'User Engagement':
            insight['charts'].extend(['rating_vs_reviews.png'])
    
    # Add overall chart list
    insights['available_charts'] = chart_files
    insights['chart_descriptions'] = chart_mapping
    
    return insights

def main():
    """Main function to enrich insights."""
    parser = argparse.ArgumentParser(description='Enrich insights with confidence scores and charts')
    parser.add_argument('--insights', required=True, help='Input insights JSON file')
    parser.add_argument('--out', required=True, help='Output enriched insights JSON file')
    
    args = parser.parse_args()
    
    try:
        # Load insights
        print(f"Loading insights from {args.insights}...")
        insights = load_insights(args.insights)
        
        # Load data for analysis
        print("Loading combined dataset...")
        df = load_combined_data()
        
        # Calculate confidence scores
        enriched_insights = calculate_confidence_scores(insights, df)
        
        # Generate charts
        chart_files = generate_charts(enriched_insights, df)
        
        # Add chart references
        enriched_insights = add_chart_references(enriched_insights, chart_files)
        
        # Save enriched insights
        print(f"Saving enriched insights to {args.out}...")
        os.makedirs(Path(args.out).parent, exist_ok=True)
        
        with open(args.out, 'w') as f:
            json.dump(enriched_insights, f, indent=2, default=str)
        
        print("Insights enrichment completed successfully!")
        print(f"Generated {len(chart_files)} supporting charts")
        print(f"Average confidence score: {np.mean([i['confidence'] for i in enriched_insights['insights']]):.2f}")
        
        return True
        
    except Exception as e:
        print(f"Error enriching insights: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
