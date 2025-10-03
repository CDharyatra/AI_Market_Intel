#!/usr/bin/env python3
"""
Central Configuration File
Contains all configuration settings, file paths, and constants for the project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# PROJECT PATHS
# ============================================================================

# Base project directory
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
CACHE_DIR = ARTIFACTS_DIR / "cache"
CHARTS_DIR = ARTIFACTS_DIR / "charts"

# Data subdirectories
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Ensure directories exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, ARTIFACTS_DIR, CACHE_DIR, CHARTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# FILE PATHS
# ============================================================================

# Raw data files
KAGGLE_CSV_PATH = RAW_DATA_DIR / "googleplaystore.csv"
KAGGLE_PARQUET_PATH = RAW_DATA_DIR / "kaggle_google_play.parquet"
RAPIDAPI_JSONL_PATH = RAW_DATA_DIR / "rapidapi_appstore.jsonl"
D2C_DATASET_PATH = PROJECT_ROOT / "Kasparro_Phase5_D2C_Synthetic_Dataset.xlsx"

# Processed data files
KAGGLE_CLEANED_PATH = PROCESSED_DATA_DIR / "kaggle_cleaned.parquet"
IOS_CLEANED_PATH = PROCESSED_DATA_DIR / "rapidapi_ios.parquet"
COMBINED_APPS_PATH = PROCESSED_DATA_DIR / "combined_apps.parquet"

# Artifact files
AGGREGATES_PATH = ARTIFACTS_DIR / "aggregates.json"
INSIGHTS_PATH = ARTIFACTS_DIR / "insights.json"
REPORT_PATH = ARTIFACTS_DIR / "report.pdf"
D2C_METRICS_PATH = ARTIFACTS_DIR / "d2c_metrics.json"
CREATIVE_OUTPUTS_PATH = ARTIFACTS_DIR / "creative_outputs.json"
NAME_MATCHES_PATH = ARTIFACTS_DIR / "name_matches.csv"

# ============================================================================
# API CONFIGURATION
# ============================================================================

# API Keys (loaded from .env file)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
KAGGLE_USERNAME = os.getenv('KAGGLE_USERNAME')
KAGGLE_KEY = os.getenv('KAGGLE_KEY')

# API Endpoints
RAPIDAPI_BASE_URL = "https://app-store-data.p.rapidapi.com"
OLLAMA_BASE_URL = "http://localhost:11434/api/generate"
FREE_AI_API_URL = "https://api.deepai.org/api/text-generator"
HUGGINGFACE_MODEL_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

# API Headers
def get_rapidapi_headers():
    """Get RapidAPI headers with API key."""
    return {
        "X-RapidAPI-Key": RAPIDAPI_KEY or "mock_key",
        "X-RapidAPI-Host": "app-store-data.p.rapidapi.com"
    }

def get_huggingface_headers():
    """Get Hugging Face headers with API key."""
    return {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# ============================================================================
# D2C CATEGORIES & MARKETING CONFIG
# ============================================================================

# D2C App Categories
D2C_CATEGORIES = [
    'Fashion & Apparel',
    'Beauty & Personal Care',
    'Home & Living',
    'Food & Beverage',
    'Health & Wellness',
    'Electronics & Gadgets',
    'Sports & Fitness',
    'Kids & Baby',
    'Pet Care',
    'Jewelry & Accessories'
]

# Marketing Channels
MARKETING_CHANNELS = [
    'Google Ads',
    'Meta Ads',
    'Instagram Ads',
    'TikTok Ads',
    'YouTube Ads',
    'Twitter Ads',
    'Snapchat Ads',
    'LinkedIn Ads',
    'Organic Search',
    'Email Marketing'
]

# SEO Categories (for opportunity analysis)
SEO_CATEGORIES = [
    'Gaming Apps',
    'Shopping Apps',
    'Social Media Apps',
    'Productivity Apps',
    'Health & Fitness Apps',
    'Education Apps',
    'Entertainment Apps',
    'Travel Apps',
    'Food Delivery Apps',
    'Finance Apps'
]

# ============================================================================
# APP STORE CATEGORIES
# ============================================================================

# iOS Categories
IOS_CATEGORIES = [
    'Games', 'Entertainment', 'Education', 'Lifestyle', 'Utilities',
    'Productivity', 'Social Networking', 'Photo & Video', 'Music',
    'Health & Fitness', 'News', 'Weather', 'Travel', 'Food & Drink',
    'Shopping', 'Finance', 'Business', 'Medical', 'Sports', 'Reference'
]

# Android Categories (Google Play)
ANDROID_CATEGORIES = [
    'ART_AND_DESIGN', 'AUTO_AND_VEHICLES', 'BEAUTY', 'BOOKS_AND_REFERENCE',
    'BUSINESS', 'COMICS', 'COMMUNICATION', 'DATING', 'EDUCATION',
    'ENTERTAINMENT', 'EVENTS', 'FINANCE', 'FOOD_AND_DRINK', 'HEALTH_AND_FITNESS',
    'HOUSE_AND_HOME', 'LIBRARIES_AND_DEMO', 'LIFESTYLE', 'GAME', 'FAMILY',
    'MEDICAL', 'SOCIAL', 'SHOPPING', 'PHOTOGRAPHY', 'SPORTS', 'TRAVEL_AND_LOCAL',
    'TOOLS', 'PERSONALIZATION', 'PRODUCTIVITY', 'PARENTING', 'WEATHER',
    'VIDEO_PLAYERS', 'NEWS_AND_MAGAZINES', 'MAPS_AND_NAVIGATION'
]

# ============================================================================
# DATA PROCESSING CONFIGURATION
# ============================================================================

# Content Rating Mapping (iOS to Android)
CONTENT_RATING_MAP = {
    '4+': 'Everyone',
    '9+': 'Everyone 10+',
    '12+': 'Teen',
    '17+': 'Mature 17+'
}

# Price Tiers
PRICE_TIERS = {
    'Free': (0, 0),
    'Budget': (0.01, 2.99),
    'Mid-Range': (3.00, 9.99),
    'Premium': (10.00, 29.99),
    'Enterprise': (30.00, float('inf'))
}

# Rating Thresholds
RATING_THRESHOLDS = {
    'Excellent': 4.5,
    'Good': 4.0,
    'Average': 3.5,
    'Below Average': 3.0,
    'Poor': 0.0
}

# Data Processing Limits
MAX_SAMPLE_SIZE = 10000  # Maximum sample size for visualizations
DEFAULT_ENCODING = 'utf-8'
FALLBACK_ENCODINGS = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

# ============================================================================
# AI INSIGHTS CONFIGURATION
# ============================================================================

# AI Model Configuration
AI_MODELS = {
    'gemini': {
        'name': 'Google Gemini',
        'model': 'gemini-pro',
        'priority': 1,
        'requires_key': True
    },
    'openai': {
        'name': 'OpenAI',
        'model': 'gpt-3.5-turbo',
        'priority': 2,
        'requires_key': True,
        'max_tokens': 2000,
        'temperature': 0.7
    },
    'huggingface': {
        'name': 'Hugging Face',
        'model': 'microsoft/DialoGPT-medium',
        'priority': 3,
        'requires_key': True
    },
    'ollama': {
        'name': 'Ollama Local',
        'model': 'llama2',
        'priority': 4,
        'requires_key': False
    }
}

# Insight Categories
INSIGHT_CATEGORIES = [
    'Market Analysis',
    'Platform Comparison',
    'Monetization',
    'User Engagement',
    'Competition',
    'Revenue Performance',
    'Channel Performance',
    'Conversion Optimization',
    'SEO Optimization',
    'Unit Economics',
    'Data Quality'
]

# Confidence Thresholds
CONFIDENCE_THRESHOLDS = {
    'High': 0.8,
    'Medium': 0.6,
    'Low': 0.0
}

# ============================================================================
# D2C FUNNEL METRICS CONFIGURATION
# ============================================================================

# Funnel Stages
FUNNEL_STAGES = [
    'impressions',
    'clicks',
    'installs',
    'signups',
    'first_purchase',
    'repeat_purchase'
]

# Performance Thresholds
PERFORMANCE_THRESHOLDS = {
    'roas': {
        'excellent': 3.0,
        'good': 2.0,
        'poor': 1.0
    },
    'ltv_cac_ratio': {
        'excellent': 3.0,
        'good': 2.0,
        'poor': 1.0
    },
    'first_purchase_rate': {
        'excellent': 15.0,
        'good': 10.0,
        'poor': 5.0
    },
    'repeat_purchase_rate': {
        'excellent': 30.0,
        'good': 20.0,
        'poor': 10.0
    }
}

# ============================================================================
# VISUALIZATION CONFIGURATION
# ============================================================================

# Chart Settings
CHART_CONFIG = {
    'default_width': 1200,
    'default_height': 600,
    'color_palette': 'viridis',
    'font_size': 12,
    'title_font_size': 16,
    'dpi': 150
}

# Chart Types
CHART_TYPES = [
    'bar', 'line', 'scatter', 'pie', 'box', 'heatmap', 'histogram'
]

# ============================================================================
# REPORT CONFIGURATION
# ============================================================================

# Report Settings
REPORT_CONFIG = {
    'title': 'AI Market Intelligence Report',
    'author': 'AI Market Intelligence System',
    'page_size': 'A4',
    'margins': {
        'top': 72,
        'bottom': 72,
        'left': 72,
        'right': 72
    },
    'font_family': 'Helvetica',
    'title_font_size': 24,
    'heading_font_size': 16,
    'body_font_size': 12
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Log Settings
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S'
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_api_key_status():
    """Check which API keys are configured."""
    return {
        'openai': bool(OPENAI_API_KEY),
        'gemini': bool(GEMINI_API_KEY),
        'huggingface': bool(HUGGINGFACE_API_KEY),
        'rapidapi': bool(RAPIDAPI_KEY),
        'kaggle': bool(KAGGLE_USERNAME and KAGGLE_KEY)
    }

def get_file_path(file_type):
    """Get file path by type."""
    paths = {
        'kaggle_csv': KAGGLE_CSV_PATH,
        'kaggle_parquet': KAGGLE_PARQUET_PATH,
        'rapidapi_jsonl': RAPIDAPI_JSONL_PATH,
        'd2c_dataset': D2C_DATASET_PATH,
        'kaggle_cleaned': KAGGLE_CLEANED_PATH,
        'ios_cleaned': IOS_CLEANED_PATH,
        'combined_apps': COMBINED_APPS_PATH,
        'aggregates': AGGREGATES_PATH,
        'insights': INSIGHTS_PATH,
        'report': REPORT_PATH,
        'd2c_metrics': D2C_METRICS_PATH,
        'creative_outputs': CREATIVE_OUTPUTS_PATH,
        'name_matches': NAME_MATCHES_PATH
    }
    return paths.get(file_type)

def validate_config():
    """Validate configuration settings."""
    errors = []
    
    # Check if critical directories exist
    for directory in [DATA_DIR, ARTIFACTS_DIR]:
        if not directory.exists():
            errors.append(f"Directory not found: {directory}")
    
    # Check if at least one AI API key is configured
    api_keys = get_api_key_status()
    if not any(api_keys.values()):
        errors.append("No AI API keys configured. The system will use data-driven insights only.")
    
    return errors

# ============================================================================
# EXPORT CONFIGURATION
# ============================================================================

__all__ = [
    # Paths
    'PROJECT_ROOT', 'DATA_DIR', 'ARTIFACTS_DIR', 'RAW_DATA_DIR', 
    'PROCESSED_DATA_DIR', 'CACHE_DIR', 'CHARTS_DIR',
    
    # File Paths
    'KAGGLE_CSV_PATH', 'KAGGLE_PARQUET_PATH', 'RAPIDAPI_JSONL_PATH',
    'D2C_DATASET_PATH', 'KAGGLE_CLEANED_PATH', 'IOS_CLEANED_PATH',
    'COMBINED_APPS_PATH', 'AGGREGATES_PATH', 'INSIGHTS_PATH',
    'REPORT_PATH', 'D2C_METRICS_PATH', 'CREATIVE_OUTPUTS_PATH',
    'NAME_MATCHES_PATH',
    
    # API Configuration
    'OPENAI_API_KEY', 'GEMINI_API_KEY', 'HUGGINGFACE_API_KEY',
    'RAPIDAPI_KEY', 'RAPIDAPI_BASE_URL', 'OLLAMA_BASE_URL',
    'get_rapidapi_headers', 'get_huggingface_headers',
    
    # Categories
    'D2C_CATEGORIES', 'MARKETING_CHANNELS', 'SEO_CATEGORIES',
    'IOS_CATEGORIES', 'ANDROID_CATEGORIES', 'INSIGHT_CATEGORIES',
    
    # Configuration Dicts
    'CONTENT_RATING_MAP', 'PRICE_TIERS', 'RATING_THRESHOLDS',
    'AI_MODELS', 'CONFIDENCE_THRESHOLDS', 'FUNNEL_STAGES',
    'PERFORMANCE_THRESHOLDS', 'CHART_CONFIG', 'REPORT_CONFIG',
    
    # Utility Functions
    'get_api_key_status', 'get_file_path', 'validate_config'
]
