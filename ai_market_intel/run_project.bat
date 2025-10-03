@echo off
echo ========================================
echo    AI Market Intelligence Project
echo ========================================
echo.

echo [1/3] Activating virtual environment...
call .venv\Scripts\activate

echo [2/3] Checking project status...
python src/cli.py status

echo.
echo [3/3] Choose an option:
echo   1. Launch Web Interface
echo   2. Show Data Statistics  
echo   3. Show Real Data Insights
echo   4. Show D2C Analysis
echo   5. Setup Gemini API (Free)
echo   6. Setup All API Keys
echo   7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    echo Launching Streamlit web interface...
    streamlit run src/ui/streamlit_app.py
) else if "%choice%"=="2" (
    echo Showing data statistics...
    python -c "import pandas as pd; df = pd.read_parquet('data/processed/combined_apps.parquet'); print(f'Total Apps: {len(df):,}'); print(f'Android: {len(df[df[\"platform\"].isin([\"Android\", \"Both\"])]):,}'); print(f'iOS: {len(df[df[\"platform\"].isin([\"iOS\", \"Both\"])]):,}'); print(f'Categories: {df[\"category\"].nunique()}'); print(f'Avg Rating: {df[\"rating\"].mean():.2f}')"
) else if "%choice%"=="3" (
    echo Showing real data insights...
    python show_ai_insights.py
) else if "%choice%"=="4" (
    echo Showing D2C analysis...
    python -c "import json; d2c = json.load(open('artifacts/d2c_metrics.json')); print(f'D2C Analysis: {d2c[\"funnel_metrics\"][\"overall_metrics\"][\"total_campaigns\"]} campaigns, ROAS: {d2c[\"funnel_metrics\"][\"revenue_metrics\"][\"roas\"]:.2f}')"
) else if "%choice%"=="5" (
    echo Setting up Gemini API...
    python setup_gemini.py
) else if "%choice%"=="6" (
    echo Setting up all API keys...
    python setup_api_keys.py
) else if "%choice%"=="7" (
    echo Goodbye!
    exit
) else (
    echo Invalid choice. Please run the script again.
)

echo.
pause
