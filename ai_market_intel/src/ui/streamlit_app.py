#!/usr/bin/env python3
"""
Streamlit Web Application for AI Market Intelligence
Interactive web interface for exploring insights and data.
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AI Market Intelligence Dashboard",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """Load all required data files."""
    data = {}
    
    # Load combined dataset
    combined_path = "data/processed/combined_apps.parquet"
    if Path(combined_path).exists():
        data['combined'] = pd.read_parquet(combined_path)
    
    # Load insights
    insights_path = "artifacts/insights.json"
    if Path(insights_path).exists():
        with open(insights_path, 'r') as f:
            data['insights'] = json.load(f)
    
    # Load aggregates
    aggregates_path = "artifacts/aggregates.json"
    if Path(aggregates_path).exists():
        with open(aggregates_path, 'r') as f:
            data['aggregates'] = json.load(f)
    
    return data

def create_sidebar():
    """Create the sidebar navigation."""
    st.sidebar.title("📱 AI Market Intelligence")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["Overview", "Insights", "Data Explorer", "Platform Comparison", "Category Analysis"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Data Status")
    
    # Check data availability
    data = load_data()
    if 'combined' in data:
        st.sidebar.success(f"✅ {len(data['combined']):,} apps loaded")
    else:
        st.sidebar.error("❌ No data loaded")
    
    if 'insights' in data:
        st.sidebar.success(f"✅ {len(data['insights']['insights'])} insights available")
    else:
        st.sidebar.warning("⚠️ No insights available")
    
    return page, data

def render_overview(data):
    """Render the overview page."""
    st.title("📊 Market Intelligence Overview")
    
    if 'aggregates' not in data:
        st.error("No data available. Please run the pipeline first.")
        return
    
    overall = data['aggregates']['overall_stats']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Apps",
            value=f"{overall['total_apps']:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Average Rating",
            value=f"{overall['avg_rating']:.2f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Paid Apps",
            value=f"{overall['paid_apps']:,}",
            delta=f"{overall['paid_apps']/overall['total_apps']*100:.1f}%"
        )
    
    with col4:
        st.metric(
            label="Categories",
            value=f"{overall['total_categories']}",
            delta=None
        )
    
    # Platform distribution
    st.subheader("Platform Distribution")
    platform_dist = overall['platform_distribution']
    
    fig = px.pie(
        values=list(platform_dist.values()),
        names=list(platform_dist.keys()),
        title="Apps by Platform"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top categories
    st.subheader("Top Categories")
    top_categories = overall['top_categories']
    
    fig = px.bar(
        x=list(top_categories.values()),
        y=list(top_categories.keys()),
        orientation='h',
        title="Top 10 Categories by App Count"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

def render_insights(data):
    """Render the insights page."""
    st.title("🧠 AI-Generated Insights")
    
    if 'insights' not in data:
        st.error("No insights available. Please generate insights first.")
        return
    
    insights = data['insights']
    
    # Summary
    st.subheader("Executive Summary")
    st.write(insights.get('summary', 'No summary available.'))
    
    # Key trends
    if 'key_trends' in insights:
        st.subheader("Key Market Trends")
        for trend in insights['key_trends']:
            st.write(f"• {trend}")
    
    st.markdown("---")
    
    # Detailed insights
    st.subheader("Detailed Insights")
    
    for i, insight in enumerate(insights['insights'], 1):
        with st.expander(f"{i}. {insight['title']}", expanded=False):
            st.write(f"**Description:** {insight['description']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Confidence:** {insight['confidence']:.0%}")
            with col2:
                st.write(f"**Category:** {insight['category']}")
            
            if 'supporting_data' in insight and insight['supporting_data']:
                st.write("**Supporting Data:**")
                for key, value in insight['supporting_data'].items():
                    if isinstance(value, (int, float)):
                        st.write(f"• {key.replace('_', ' ').title()}: {value:,.2f}")
                    else:
                        st.write(f"• {key.replace('_', ' ').title()}: {value}")
            
            if 'implications' in insight:
                st.write(f"**Implications:** {insight['implications']}")
            
            if 'recommendations' in insight:
                st.write(f"**Recommendations:** {insight['recommendations']}")

def render_data_explorer(data):
    """Render the data explorer page."""
    st.title("🔍 Data Explorer")
    
    if 'combined' not in data:
        st.error("No data available. Please run the pipeline first.")
        return
    
    df = data['combined']
    
    # Filters
    st.subheader("Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        platforms = st.multiselect(
            "Platform",
            options=df['platform'].unique(),
            default=df['platform'].unique()
        )
    
    with col2:
        categories = st.multiselect(
            "Category",
            options=df['category'].unique(),
            default=df['category'].unique()
        )
    
    with col3:
        price_range = st.slider(
            "Price Range (USD)",
            min_value=0.0,
            max_value=float(df['price_usd'].max()),
            value=(0.0, float(df['price_usd'].max())),
            step=0.01
        )
    
    # Apply filters
    filtered_df = df[
        (df['platform'].isin(platforms)) &
        (df['category'].isin(categories)) &
        (df['price_usd'] >= price_range[0]) &
        (df['price_usd'] <= price_range[1])
    ]
    
    st.write(f"Showing {len(filtered_df):,} apps (filtered from {len(df):,})")
    
    # Data table
    st.subheader("App Data")
    
    # Select columns to display
    display_columns = st.multiselect(
        "Select columns to display:",
        options=df.columns.tolist(),
        default=['app_name', 'platform', 'category', 'rating', 'reviews', 'price_usd']
    )
    
    if display_columns:
        st.dataframe(
            filtered_df[display_columns].head(1000),
            use_container_width=True,
            height=400
        )
    
    # Download option
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="filtered_apps.csv",
        mime="text/csv"
    )

def render_platform_comparison(data):
    """Render the platform comparison page."""
    st.title("📱 Platform Comparison")
    
    if 'combined' not in data:
        st.error("No data available. Please run the pipeline first.")
        return
    
    df = data['combined']
    
    # Platform metrics comparison
    st.subheader("Platform Metrics")
    
    platform_metrics = df.groupby('platform').agg({
        'rating': ['mean', 'median', 'std'],
        'reviews': ['mean', 'sum'],
        'price_usd': ['mean', 'median'],
        'installs': ['mean', 'sum']
    }).round(2)
    
    st.dataframe(platform_metrics, use_container_width=True)
    
    # Rating comparison
    st.subheader("Rating Distribution by Platform")
    
    fig = px.box(
        df,
        x='platform',
        y='rating',
        title="App Ratings by Platform"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Price comparison
    st.subheader("Price Distribution by Platform")
    
    paid_apps = df[df['price_usd'] > 0]
    if len(paid_apps) > 0:
        fig = px.box(
            paid_apps,
            x='platform',
            y='price_usd',
            title="Paid App Prices by Platform"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Reviews vs Rating scatter
    st.subheader("Reviews vs Rating by Platform")
    
    sample_df = df.sample(min(5000, len(df)))
    fig = px.scatter(
        sample_df,
        x='reviews',
        y='rating',
        color='platform',
        title="Reviews vs Rating by Platform",
        log_x=True
    )
    st.plotly_chart(fig, use_container_width=True)

def render_category_analysis(data):
    """Render the category analysis page."""
    st.title("📂 Category Analysis")
    
    if 'combined' not in data:
        st.error("No data available. Please run the pipeline first.")
        return
    
    df = data['combined']
    
    # Category performance
    st.subheader("Category Performance")
    
    category_stats = df.groupby('category').agg({
        'rating': 'mean',
        'reviews': 'sum',
        'price_usd': 'mean',
        'app_name': 'count'
    }).round(2)
    
    category_stats.columns = ['Avg Rating', 'Total Reviews', 'Avg Price', 'App Count']
    category_stats = category_stats.sort_values('App Count', ascending=False)
    
    st.dataframe(category_stats.head(20), use_container_width=True)
    
    # Top categories by different metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Categories by App Count")
        top_by_count = category_stats.head(10)
        
        fig = px.bar(
            x=top_by_count['App Count'],
            y=top_by_count.index,
            orientation='h',
            title="Top 10 Categories by App Count"
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Categories by Average Rating")
        top_by_rating = category_stats.sort_values('Avg Rating', ascending=False).head(10)
        
        fig = px.bar(
            x=top_by_rating['Avg Rating'],
            y=top_by_rating.index,
            orientation='h',
            title="Top 10 Categories by Average Rating"
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Category vs Platform heatmap
    st.subheader("Category Distribution by Platform")
    
    category_platform = pd.crosstab(df['category'], df['platform'])
    category_platform = category_platform.head(15)  # Top 15 categories
    
    fig = px.imshow(
        category_platform,
        title="Category Distribution by Platform (Top 15 Categories)",
        aspect="auto"
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application function."""
    # Create sidebar and load data
    page, data = create_sidebar()
    
    # Render the selected page
    if page == "Overview":
        render_overview(data)
    elif page == "Insights":
        render_insights(data)
    elif page == "Data Explorer":
        render_data_explorer(data)
    elif page == "Platform Comparison":
        render_platform_comparison(data)
    elif page == "Category Analysis":
        render_category_analysis(data)
    
    # Footer
    st.markdown("---")
    st.markdown("**AI Market Intelligence Dashboard** - Powered by Streamlit")

if __name__ == "__main__":
    main()
