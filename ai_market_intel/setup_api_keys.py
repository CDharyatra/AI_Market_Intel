#!/usr/bin/env python3
"""
API Keys Setup Script
Helps users set up free API keys for AI insights generation.
"""

import os
import sys
import shutil
import requests
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / 'src'))
from config import get_api_key_status, PROJECT_ROOT

def create_env_file():
    """Create .env file from .env.example template."""
    env_path = PROJECT_ROOT / ".env"
    env_example_path = PROJECT_ROOT / ".env.example"
    
    if env_path.exists():
        print("ℹ️  .env file already exists")
        return
    
    if env_example_path.exists():
        # Copy .env.example to .env
        shutil.copy(env_example_path, env_path)
        print("✅ Created .env file from .env.example template")
        print("📝 Please edit .env file and add your API keys")
    else:
        print("⚠️  .env.example not found. Creating basic .env file...")
        # Create a basic .env file
        with open(env_path, 'w') as f:
            f.write("# AI Market Intelligence - API Keys\n")
            f.write("# Add your API keys below\n\n")
            f.write("GEMINI_API_KEY=\n")
            f.write("# OPENAI_API_KEY=\n")
            f.write("# HUGGINGFACE_API_KEY=\n")
            f.write("# RAPIDAPI_KEY=\n")
        print("✅ Created basic .env file")

def test_api_connections():
    """Test available API connections."""
    print("\n🔍 Testing API connections...")
    
    # Use centralized config to check API keys
    api_status = get_api_key_status()
    
    # Test Gemini
    if api_status['gemini']:
        print("✅ Google Gemini API key found")
    else:
        print("❌ Google Gemini API key not found")
    
    # Test OpenAI
    if api_status['openai']:
        print("✅ OpenAI API key found")
    else:
        print("❌ OpenAI API key not found")
    
    # Test Hugging Face
    if api_status['huggingface']:
        print("✅ Hugging Face API key found")
    else:
        print("❌ Hugging Face API key not found")
    
    # Test RapidAPI
    if api_status['rapidapi']:
        print("✅ RapidAPI key found")
    else:
        print("❌ RapidAPI key not found")
    
    # Test Kaggle
    if api_status['kaggle']:
        print("✅ Kaggle credentials found")
    else:
        print("❌ Kaggle credentials not found")

def show_setup_instructions():
    """Show instructions for getting free API keys."""
    print("\n📋 FREE API KEY SETUP INSTRUCTIONS:")
    print("=" * 50)
    
    print("\n1. GOOGLE GEMINI API (Recommended - Easiest & Free):")
    print("   • Visit: https://aistudio.google.com/app/apikey")
    print("   • Sign in with Google account")
    print("   • Click 'Create API Key'")
    print("   • No credit card required!")
    print("   • Add key to .env file: GEMINI_API_KEY=your_key_here")
    print("   • Or run: python setup_gemini.py")
    
    print("\n2. OPENAI API (Alternative):")
    print("   • Visit: https://platform.openai.com/api-keys")
    print("   • Sign up for free account")
    print("   • Get $5 free credits (enough for many requests)")
    print("   • Add key to .env file: OPENAI_API_KEY=your_key_here")
    
    print("\n3. HUGGING FACE API (Free):")
    print("   • Visit: https://huggingface.co/settings/tokens")
    print("   • Sign up for free account")
    print("   • Create new token")
    print("   • Add key to .env file: HUGGINGFACE_API_KEY=your_token_here")
    
    print("\n4. RAPIDAPI (Optional - for iOS data):")
    print("   • Visit: https://rapidapi.com/")
    print("   • Sign up for free account")
    print("   • Get free tier access")
    print("   • Add key to .env file: RAPIDAPI_KEY=your_key_here")
    
    print("\n5. LOCAL OLLAMA (Advanced - Free):")
    print("   • Install Ollama: https://ollama.ai/")
    print("   • Run: ollama pull llama2")
    print("   • Start: ollama serve")
    print("   • No API key needed - runs locally")

def show_usage_instructions():
    """Show how to use the system."""
    print("\n🚀 USAGE INSTRUCTIONS:")
    print("=" * 30)
    
    print("\n1. Set up API keys (see above)")
    print("2. Run the pipeline:")
    print("   python src/cli.py run_pipeline")
    print("\n3. Or use the batch file:")
    print("   run_project.bat")
    print("\n4. The system will try APIs in this order:")
    print("   • OpenAI (if key provided)")
    print("   • Hugging Face (if key provided)")
    print("   • Local Ollama (if running)")
    print("   • Free AI API (fallback)")
    print("   • Data-driven insights (always works)")

def main():
    """Main setup function."""
    print("🤖 AI Market Intelligence - API Setup")
    print("=" * 40)
    
    # Create .env file from template
    create_env_file()
    
    # Show setup instructions
    show_setup_instructions()
    
    # Test current connections
    test_api_connections()
    
    # Show usage instructions
    show_usage_instructions()
    
    print("\n✅ Setup complete! The system will work with or without API keys.")
    print("   Without API keys: Uses data-driven insights from real data")
    print("   With API keys: Uses AI-generated insights + real data")
    print("\n📄 Configuration files:")
    print("   • .env - Your API keys (never commit this!)")
    print("   • .env.example - Template for API keys")
    print("   • src/config.py - Centralized configuration")
    print("\n🔒 Security: Make sure .env is in your .gitignore file!")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables
    main()
