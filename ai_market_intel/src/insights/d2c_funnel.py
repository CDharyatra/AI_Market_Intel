#!/usr/bin/env python3
"""
D2C Funnel Analysis Script
Analyzes the D2C synthetic dataset to compute funnel metrics and insights.
"""

import pandas as pd
import numpy as np
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config import D2C_DATASET_PATH, D2C_METRICS_PATH, PERFORMANCE_THRESHOLDS, FUNNEL_STAGES

def load_d2c_data(filepath: str) -> pd.DataFrame:
    """Load the D2C synthetic dataset."""
    print(f"Loading D2C data from {filepath}...")
    df = pd.read_excel(filepath)
    print(f"Loaded {len(df)} campaigns")
    return df

def calculate_funnel_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate comprehensive funnel metrics."""
    print("Calculating funnel metrics...")
    
    # Overall funnel metrics
    total_spend = df['spend_usd'].sum()
    total_impressions = df['impressions'].sum()
    total_clicks = df['clicks'].sum()
    total_installs = df['installs'].sum()
    total_signups = df['signups'].sum()
    total_first_purchases = df['first_purchase'].sum()
    total_repeat_purchases = df['repeat_purchase'].sum()
    total_revenue = df['revenue_usd'].sum()
    
    # Conversion rates
    ctr = (total_clicks / total_impressions) * 100 if total_impressions > 0 else 0
    install_rate = (total_installs / total_clicks) * 100 if total_clicks > 0 else 0
    signup_rate = (total_signups / total_installs) * 100 if total_installs > 0 else 0
    first_purchase_rate = (total_first_purchases / total_signups) * 100 if total_signups > 0 else 0
    repeat_purchase_rate = (total_repeat_purchases / total_first_purchases) * 100 if total_first_purchases > 0 else 0
    
    # Revenue metrics
    roas = total_revenue / total_spend if total_spend > 0 else 0
    cac = total_spend / total_first_purchases if total_first_purchases > 0 else 0
    ltv = total_revenue / total_first_purchases if total_first_purchases > 0 else 0
    ltv_cac_ratio = ltv / cac if cac > 0 else 0
    
    # Cost per metrics
    cpm = (total_spend / total_impressions) * 1000 if total_impressions > 0 else 0
    cpc = total_spend / total_clicks if total_clicks > 0 else 0
    cpi = total_spend / total_installs if total_installs > 0 else 0
    cps = total_spend / total_signups if total_signups > 0 else 0
    
    return {
        'overall_metrics': {
            'total_campaigns': len(df),
            'total_spend_usd': total_spend,
            'total_revenue_usd': total_revenue,
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_installs': total_installs,
            'total_signups': total_signups,
            'total_first_purchases': total_first_purchases,
            'total_repeat_purchases': total_repeat_purchases
        },
        'conversion_rates': {
            'ctr_percent': ctr,
            'install_rate_percent': install_rate,
            'signup_rate_percent': signup_rate,
            'first_purchase_rate_percent': first_purchase_rate,
            'repeat_purchase_rate_percent': repeat_purchase_rate
        },
        'revenue_metrics': {
            'roas': roas,
            'cac_usd': cac,
            'ltv_usd': ltv,
            'ltv_cac_ratio': ltv_cac_ratio
        },
        'cost_metrics': {
            'cpm_usd': cpm,
            'cpc_usd': cpc,
            'cpi_usd': cpi,
            'cps_usd': cps
        }
    }

def analyze_by_channel(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze funnel metrics by channel."""
    print("Analyzing metrics by channel...")
    
    channel_analysis = {}
    
    for channel in df['channel'].unique():
        channel_data = df[df['channel'] == channel]
        
        # Calculate metrics for this channel
        total_spend = channel_data['spend_usd'].sum()
        total_revenue = channel_data['revenue_usd'].sum()
        total_first_purchases = channel_data['first_purchase'].sum()
        
        # Conversion rates
        ctr = (channel_data['clicks'].sum() / channel_data['impressions'].sum()) * 100
        install_rate = (channel_data['installs'].sum() / channel_data['clicks'].sum()) * 100
        signup_rate = (channel_data['signups'].sum() / channel_data['installs'].sum()) * 100
        first_purchase_rate = (channel_data['first_purchase'].sum() / channel_data['signups'].sum()) * 100
        
        # Revenue metrics
        roas = total_revenue / total_spend if total_spend > 0 else 0
        cac = total_spend / total_first_purchases if total_first_purchases > 0 else 0
        
        channel_analysis[channel] = {
            'campaigns': len(channel_data),
            'total_spend_usd': total_spend,
            'total_revenue_usd': total_revenue,
            'total_first_purchases': total_first_purchases,
            'ctr_percent': ctr,
            'install_rate_percent': install_rate,
            'signup_rate_percent': signup_rate,
            'first_purchase_rate_percent': first_purchase_rate,
            'roas': roas,
            'cac_usd': cac
        }
    
    return channel_analysis

def analyze_seo_opportunities(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze SEO opportunities based on search volume and position."""
    print("Analyzing SEO opportunities...")
    
    seo_analysis = {}
    
    for category in df['seo_category'].unique():
        category_data = df[df['seo_category'] == category]
        
        avg_position = category_data['avg_position'].mean()
        avg_search_volume = category_data['monthly_search_volume'].mean()
        avg_conversion_rate = category_data['conversion_rate'].mean()
        
        # Calculate opportunity score (higher search volume + lower position = higher opportunity)
        opportunity_score = (avg_search_volume / 1000) * (10 - avg_position) * avg_conversion_rate
        
        seo_analysis[category] = {
            'avg_position': avg_position,
            'avg_search_volume': avg_search_volume,
            'avg_conversion_rate': avg_conversion_rate,
            'opportunity_score': opportunity_score,
            'campaigns': len(category_data)
        }
    
    # Sort by opportunity score
    sorted_seo = sorted(seo_analysis.items(), key=lambda x: x[1]['opportunity_score'], reverse=True)
    
    return {
        'by_category': dict(sorted_seo),
        'top_opportunities': sorted_seo[:5],
        'summary': {
            'total_categories': len(seo_analysis),
            'avg_position': df['avg_position'].mean(),
            'total_search_volume': df['monthly_search_volume'].sum(),
            'avg_conversion_rate': df['conversion_rate'].mean()
        }
    }

def identify_top_performers(df: pd.DataFrame) -> Dict[str, Any]:
    """Identify top performing campaigns and channels."""
    print("Identifying top performers...")
    
    # Top campaigns by ROAS
    df['roas'] = df['revenue_usd'] / df['spend_usd']
    top_roas_campaigns = df.nlargest(5, 'roas')[['campaign_id', 'channel', 'roas', 'revenue_usd', 'spend_usd']].to_dict('records')
    
    # Top campaigns by conversion rate
    top_conversion_campaigns = df.nlargest(5, 'conversion_rate')[['campaign_id', 'channel', 'conversion_rate', 'revenue_usd']].to_dict('records')
    
    # Top channels by total revenue
    channel_revenue = df.groupby('channel')['revenue_usd'].sum().sort_values(ascending=False)
    top_revenue_channels = channel_revenue.head(3).to_dict()
    
    # Top channels by ROAS
    channel_roas = df.groupby('channel').apply(lambda x: x['revenue_usd'].sum() / x['spend_usd'].sum()).sort_values(ascending=False)
    top_roas_channels = channel_roas.head(3).to_dict()
    
    return {
        'top_roas_campaigns': top_roas_campaigns,
        'top_conversion_campaigns': top_conversion_campaigns,
        'top_revenue_channels': top_revenue_channels,
        'top_roas_channels': top_roas_channels
    }

def generate_insights(funnel_metrics: Dict[str, Any], channel_analysis: Dict[str, Any], 
                     seo_analysis: Dict[str, Any], top_performers: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate actionable insights from the analysis."""
    print("Generating D2C insights...")
    
    insights = []
    
    # ROAS insight
    overall_roas = funnel_metrics['revenue_metrics']['roas']
    if overall_roas > 3:
        insights.append({
            'title': 'Strong Overall ROAS Performance',
            'description': f'The overall ROAS of {overall_roas:.2f} indicates healthy return on ad spend.',
            'category': 'Revenue Performance',
            'confidence': 0.9,
            'recommendation': 'Continue current strategy and consider scaling successful campaigns.'
        })
    elif overall_roas < 2:
        insights.append({
            'title': 'Low ROAS Requires Optimization',
            'description': f'The overall ROAS of {overall_roas:.2f} suggests need for campaign optimization.',
            'category': 'Revenue Performance',
            'confidence': 0.85,
            'recommendation': 'Review and optimize underperforming campaigns, focus on high-converting channels.'
        })
    
    # Channel performance insight
    best_channel = max(channel_analysis.items(), key=lambda x: x[1]['roas'])
    worst_channel = min(channel_analysis.items(), key=lambda x: x[1]['roas'])
    
    insights.append({
        'title': f'{best_channel[0]} Outperforms Other Channels',
        'description': f'{best_channel[0]} shows ROAS of {best_channel[1]["roas"]:.2f} vs {worst_channel[0]} at {worst_channel[1]["roas"]:.2f}.',
        'category': 'Channel Performance',
        'confidence': 0.8,
        'recommendation': f'Increase budget allocation to {best_channel[0]} and optimize {worst_channel[0]} campaigns.'
    })
    
    # Conversion funnel insight
    first_purchase_rate = funnel_metrics['conversion_rates']['first_purchase_rate_percent']
    if first_purchase_rate < 10:
        insights.append({
            'title': 'Low First Purchase Conversion Rate',
            'description': f'Only {first_purchase_rate:.1f}% of signups convert to first purchase.',
            'category': 'Conversion Optimization',
            'confidence': 0.9,
            'recommendation': 'Improve onboarding flow, add urgency, or optimize pricing strategy.'
        })
    
    # SEO opportunity insight
    if seo_analysis['top_opportunities']:
        top_opportunity = seo_analysis['top_opportunities'][0]
        insights.append({
            'title': f'High SEO Opportunity in {top_opportunity[0]}',
            'description': f'{top_opportunity[0]} has high search volume ({top_opportunity[1]["avg_search_volume"]:,.0f}) and good conversion rate ({top_opportunity[1]["avg_conversion_rate"]:.1f}%).',
            'category': 'SEO Optimization',
            'confidence': 0.75,
            'recommendation': f'Focus SEO efforts on {top_opportunity[0]} to capture more organic traffic.'
        })
    
    # CAC vs LTV insight
    ltv_cac_ratio = funnel_metrics['revenue_metrics']['ltv_cac_ratio']
    if ltv_cac_ratio > 3:
        insights.append({
            'title': 'Healthy LTV:CAC Ratio',
            'description': f'LTV:CAC ratio of {ltv_cac_ratio:.1f} indicates sustainable unit economics.',
            'category': 'Unit Economics',
            'confidence': 0.85,
            'recommendation': 'Consider increasing acquisition spend to scale growth.'
        })
    elif ltv_cac_ratio < 2:
        insights.append({
            'title': 'Low LTV:CAC Ratio Concerns',
            'description': f'LTV:CAC ratio of {ltv_cac_ratio:.1f} suggests unit economics need improvement.',
            'category': 'Unit Economics',
            'confidence': 0.9,
            'recommendation': 'Focus on improving LTV through retention or reducing CAC through optimization.'
        })
    
    return insights

def main():
    """Main function to run D2C funnel analysis."""
    print("Starting D2C funnel analysis...")
    
    try:
        # Load data using configured path
        df = load_d2c_data(str(D2C_DATASET_PATH))
        
        # Calculate metrics
        funnel_metrics = calculate_funnel_metrics(df)
        channel_analysis = analyze_by_channel(df)
        seo_analysis = analyze_seo_opportunities(df)
        top_performers = identify_top_performers(df)
        
        # Generate insights
        insights = generate_insights(funnel_metrics, channel_analysis, seo_analysis, top_performers)
        
        # Combine all results
        d2c_results = {
            'funnel_metrics': funnel_metrics,
            'channel_analysis': channel_analysis,
            'seo_analysis': seo_analysis,
            'top_performers': top_performers,
            'insights': insights,
            'analysis_timestamp': pd.Timestamp.now().isoformat()
        }
        
        # Save results using configured path
        D2C_METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(D2C_METRICS_PATH, 'w') as f:
            json.dump(d2c_results, f, indent=2, default=str)
        
        print(f"D2C analysis completed successfully!")
        print(f"Results saved to {D2C_METRICS_PATH}")
        
        # Print summary
        print(f"\nD2C Analysis Summary:")
        print(f"Total campaigns: {funnel_metrics['overall_metrics']['total_campaigns']}")
        print(f"Total spend: ${funnel_metrics['overall_metrics']['total_spend_usd']:,.2f}")
        print(f"Total revenue: ${funnel_metrics['overall_metrics']['total_revenue_usd']:,.2f}")
        print(f"Overall ROAS: {funnel_metrics['revenue_metrics']['roas']:.2f}")
        print(f"LTV:CAC ratio: {funnel_metrics['revenue_metrics']['ltv_cac_ratio']:.1f}")
        print(f"Generated {len(insights)} insights")
        
        return True
        
    except Exception as e:
        print(f"Error during D2C analysis: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
