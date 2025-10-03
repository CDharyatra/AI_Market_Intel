#!/usr/bin/env python3
"""
Creative Generation Script
Generates SEO opportunities and marketing creatives based on D2C data and app insights.
"""

import json
import pandas as pd
import os
from pathlib import Path
from typing import Dict, List, Any
import random

def load_d2c_data():
    """Load D2C metrics and data."""
    d2c_path = "artifacts/d2c_metrics.json"
    if not Path(d2c_path).exists():
        raise FileNotFoundError(f"D2C metrics not found: {d2c_path}")
    
    with open(d2c_path, 'r') as f:
        return json.load(f)

def load_app_insights():
    """Load app store insights."""
    insights_path = "artifacts/insights.json"
    if not Path(insights_path).exists():
        raise FileNotFoundError(f"App insights not found: {insights_path}")
    
    with open(insights_path, 'r') as f:
        return json.load(f)

def generate_seo_opportunities(d2c_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate SEO opportunities based on D2C data."""
    print("Generating SEO opportunities...")
    
    seo_opportunities = []
    seo_analysis = d2c_data.get('seo_analysis', {})
    
    # Get top SEO opportunities
    top_opportunities = seo_analysis.get('top_opportunities', [])
    
    for category, data in top_opportunities[:5]:  # Top 5 opportunities
        # Generate meta descriptions
        meta_descriptions = [
            f"Discover the best {category.lower()} apps with high ratings and great reviews. Download now!",
            f"Top-rated {category.lower()} mobile apps that users love. Find your perfect app today.",
            f"Explore premium {category.lower()} apps with excellent user experience and features.",
            f"Get the most popular {category.lower()} apps with thousands of downloads and 5-star ratings."
        ]
        
        # Generate ad headlines
        ad_headlines = [
            f"Best {category} Apps - 4.5+ Stars",
            f"Top {category} Apps - Download Free",
            f"Premium {category} Apps - User Favorites",
            f"Popular {category} Apps - High Rated",
            f"Must-Have {category} Apps - Trending Now"
        ]
        
        # Generate product description blurbs
        pdp_blurbs = [
            f"Experience the best {category.lower()} apps with our curated selection of top-rated mobile applications. These apps have been carefully chosen based on user ratings, reviews, and performance metrics.",
            f"Discover premium {category.lower()} mobile apps that combine excellent functionality with outstanding user experience. Our selection features only the highest-rated apps with proven track records.",
            f"Find your next favorite {category.lower()} app from our collection of top-performing mobile applications. Each app has been vetted for quality, user satisfaction, and market performance.",
            f"Explore the most popular {category.lower()} apps that users can't stop talking about. These apps have earned their place through exceptional ratings and user engagement."
        ]
        
        # Generate keyword suggestions
        keywords = [
            f"{category.lower()} apps",
            f"best {category.lower()} mobile apps",
            f"top rated {category.lower()} apps",
            f"{category.lower()} app store",
            f"premium {category.lower()} apps",
            f"popular {category.lower()} apps",
            f"{category.lower()} app reviews",
            f"free {category.lower()} apps"
        ]
        
        opportunity = {
            'category': category,
            'search_volume': data['avg_search_volume'],
            'current_position': data['avg_position'],
            'conversion_rate': data['avg_conversion_rate'],
            'opportunity_score': data['opportunity_score'],
            'meta_descriptions': meta_descriptions,
            'ad_headlines': ad_headlines,
            'pdp_blurbs': pdp_blurbs,
            'keywords': keywords,
            'priority': 'High' if data['opportunity_score'] > 100 else 'Medium' if data['opportunity_score'] > 50 else 'Low'
        }
        
        seo_opportunities.append(opportunity)
    
    return seo_opportunities

def generate_ad_creatives(d2c_data: Dict[str, Any], app_insights: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate ad creatives based on D2C and app data."""
    print("Generating ad creatives...")
    
    ad_creatives = []
    
    # Get top performing channels from D2C data
    channel_analysis = d2c_data.get('channel_analysis', {})
    top_channels = sorted(channel_analysis.items(), key=lambda x: x[1]['roas'], reverse=True)
    
    # Get insights about app performance
    app_insights_list = app_insights.get('insights', [])
    
    for channel, metrics in top_channels[:3]:  # Top 3 channels
        # Generate channel-specific creatives
        if 'Instagram' in channel:
            creative_type = 'Visual Social Media'
            formats = ['Story', 'Feed Post', 'Reel', 'IGTV']
        elif 'Google' in channel:
            creative_type = 'Search Ads'
            formats = ['Text Ad', 'Display Ad', 'Shopping Ad']
        elif 'Meta' in channel:
            creative_type = 'Social Media'
            formats = ['Feed Post', 'Story', 'Video Ad', 'Carousel']
        else:
            creative_type = 'General'
            formats = ['Banner', 'Text', 'Video']
        
        # Generate headlines based on app insights
        headlines = []
        for insight in app_insights_list[:3]:  # Use top 3 insights
            if 'iOS' in insight['title'] and 'Rating' in insight['title']:
                headlines.extend([
                    "iOS Apps Get Higher Ratings - Download Now!",
                    "Why iOS Users Love Our Apps - Try Today",
                    "4.5+ Star iOS Apps - Join the Trend"
                ])
            elif 'Gaming' in insight['title']:
                headlines.extend([
                    "Join the Gaming Revolution - Top Apps",
                    "Gaming Apps That Dominate the Charts",
                    "Why Gamers Choose Our Apps - Download Free"
                ])
            elif 'Free' in insight['title']:
                headlines.extend([
                    "Free Apps That Beat Paid Ones - Download Now",
                    "Why Free Apps Dominate - Try Ours",
                    "Premium Quality, Zero Cost - Get Started"
                ])
        
        # Generate descriptions
        descriptions = [
            "Discover apps that users can't stop downloading. Join millions who trust our recommendations.",
            "Experience the difference quality makes. Our apps consistently outperform the competition.",
            "Don't settle for average apps. Get the best-rated, most-loved mobile applications.",
            "Why choose our apps? Because users consistently rate them higher and engage more.",
            "Join the community of smart users who choose quality over quantity every time."
        ]
        
        # Generate call-to-actions
        ctas = [
            "Download Now",
            "Get Started Free",
            "Try Today",
            "Download Free",
            "Get the App",
            "Start Now",
            "Download Here",
            "Get Started"
        ]
        
        creative = {
            'channel': channel,
            'creative_type': creative_type,
            'formats': formats,
            'headlines': headlines[:5],  # Top 5 headlines
            'descriptions': descriptions[:3],  # Top 3 descriptions
            'ctas': ctas,
            'roas': metrics['roas'],
            'recommended_budget': f"${metrics['total_spend_usd'] * 1.2:,.0f}",  # 20% increase
            'target_audience': f"High-intent users interested in {channel.lower()} content"
        }
        
        ad_creatives.append(creative)
    
    return ad_creatives

def generate_content_ideas(d2c_data: Dict[str, Any], app_insights: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate content ideas for marketing."""
    print("Generating content ideas...")
    
    content_ideas = []
    
    # Blog post ideas
    blog_ideas = [
        "The Complete Guide to Choosing the Best Mobile Apps in 2024",
        "Why iOS Apps Consistently Outperform Android Apps: A Data Analysis",
        "The Hidden Psychology Behind Free vs Paid App Success",
        "How Cross-Platform Apps Are Dominating the Market",
        "The ROI of App Store Optimization: A Marketer's Guide",
        "Why Gaming Apps Rule the App Store: Market Insights",
        "The Science of App Ratings: What Makes Users Give 5 Stars",
        "From Download to Purchase: Optimizing Your App Funnel"
    ]
    
    # Video content ideas
    video_ideas = [
        "App Store vs Google Play: Which Platform Performs Better?",
        "The Secret to High App Ratings (Revealed by Data)",
        "Why Some Apps Go Viral While Others Don't",
        "The Psychology of App Downloads: What Users Really Want",
        "Cross-Platform App Development: Success Stories",
        "The Future of Mobile Apps: Trends and Predictions",
        "App Monetization Strategies That Actually Work",
        "User Experience vs App Performance: Finding the Balance"
    ]
    
    # Social media content ideas
    social_ideas = [
        "App Store Statistics That Will Blow Your Mind",
        "The Most Downloaded App Categories of 2024",
        "Why Users Choose iOS Over Android (Data-Backed)",
        "The Evolution of Mobile App Design",
        "App Store Success Stories: From Zero to Hero",
        "The Psychology Behind App Store Reviews",
        "Cross-Platform Apps: The Future of Mobile",
        "App Monetization: Free vs Paid Strategies"
    ]
    
    # Email campaign ideas
    email_ideas = [
        "Weekly App Store Insights: What's Trending",
        "App Performance Report: Your Monthly Digest",
        "New App Launches: Don't Miss These Gems",
        "App Store Optimization Tips: Expert Roundup",
        "User Behavior Analysis: What the Data Shows",
        "App Marketing Trends: Stay Ahead of the Curve",
        "Success Stories: Apps That Made It Big",
        "App Store Algorithm Updates: What You Need to Know"
    ]
    
    content_ideas = [
        {
            'type': 'Blog Posts',
            'ideas': blog_ideas,
            'target_audience': 'App developers, marketers, tech enthusiasts',
            'estimated_effort': '2-4 hours per post',
            'seo_potential': 'High'
        },
        {
            'type': 'Video Content',
            'ideas': video_ideas,
            'target_audience': 'App developers, mobile marketers',
            'estimated_effort': '4-8 hours per video',
            'seo_potential': 'Very High'
        },
        {
            'type': 'Social Media',
            'ideas': social_ideas,
            'target_audience': 'General mobile app users',
            'estimated_effort': '30-60 minutes per post',
            'seo_potential': 'Medium'
        },
        {
            'type': 'Email Campaigns',
            'ideas': email_ideas,
            'target_audience': 'App store subscribers, newsletter readers',
            'estimated_effort': '1-2 hours per campaign',
            'seo_potential': 'Low'
        }
    ]
    
    return content_ideas

def generate_landing_page_ideas(d2c_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate landing page ideas based on D2C data."""
    print("Generating landing page ideas...")
    
    landing_pages = []
    
    # Get top performing categories from D2C data
    seo_analysis = d2c_data.get('seo_analysis', {})
    top_categories = seo_analysis.get('top_opportunities', [])[:5]
    
    for category, data in top_categories:
        landing_page = {
            'title': f"Best {category} Apps - Top Rated & Most Downloaded",
            'url_slug': f"best-{category.lower().replace(' ', '-')}-apps",
            'meta_description': f"Discover the highest-rated {category.lower()} apps with thousands of downloads. Our curated list features only the best mobile applications.",
            'headline': f"Find the Perfect {category} App for You",
            'subheadline': f"Browse our collection of top-rated {category.lower()} apps, carefully selected based on user ratings, reviews, and performance metrics.",
            'key_benefits': [
                f"Curated selection of top {category.lower()} apps",
                "Based on real user ratings and reviews",
                "Updated regularly with new releases",
                "Free and paid options available",
                "Cross-platform compatibility"
            ],
            'cta_primary': "Browse Apps Now",
            'cta_secondary': "View All Categories",
            'target_keywords': [
                f"{category.lower()} apps",
                f"best {category.lower()} mobile apps",
                f"top rated {category.lower()} apps",
                f"{category.lower()} app store",
                f"premium {category.lower()} apps"
            ],
            'estimated_traffic': f"{data['avg_search_volume']:,.0f} monthly searches",
            'competition_level': 'High' if data['avg_position'] < 3 else 'Medium' if data['avg_position'] < 6 else 'Low'
        }
        
        landing_pages.append(landing_page)
    
    return landing_pages

def main():
    """Main function to generate all creatives."""
    print("Starting creative generation...")
    
    try:
        # Load data
        d2c_data = load_d2c_data()
        app_insights = load_app_insights()
        
        # Generate all creative types
        seo_opportunities = generate_seo_opportunities(d2c_data)
        ad_creatives = generate_ad_creatives(d2c_data, app_insights)
        content_ideas = generate_content_ideas(d2c_data, app_insights)
        landing_pages = generate_landing_page_ideas(d2c_data)
        
        # Combine all creative outputs
        creative_outputs = {
            'seo_opportunities': seo_opportunities,
            'ad_creatives': ad_creatives,
            'content_ideas': content_ideas,
            'landing_pages': landing_pages,
            'generation_timestamp': pd.Timestamp.now().isoformat(),
            'summary': {
                'total_seo_opportunities': len(seo_opportunities),
                'total_ad_creatives': len(ad_creatives),
                'total_content_ideas': sum(len(ci['ideas']) for ci in content_ideas),
                'total_landing_pages': len(landing_pages)
            }
        }
        
        # Save results
        output_path = "artifacts/creative_outputs.json"
        os.makedirs(Path(output_path).parent, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(creative_outputs, f, indent=2, default=str)
        
        print(f"Creative generation completed successfully!")
        print(f"Results saved to {output_path}")
        
        # Print summary
        print(f"\nCreative Generation Summary:")
        print(f"SEO opportunities: {len(seo_opportunities)}")
        print(f"Ad creative sets: {len(ad_creatives)}")
        print(f"Content ideas: {creative_outputs['summary']['total_content_ideas']}")
        print(f"Landing page concepts: {len(landing_pages)}")
        
        return True
        
    except Exception as e:
        print(f"Error during creative generation: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
