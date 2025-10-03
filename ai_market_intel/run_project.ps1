# AI Market Intelligence Project - PowerShell Launcher
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AI Market Intelligence Project" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Activating virtual environment..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1

Write-Host "[2/3] Checking project status..." -ForegroundColor Yellow
python src/cli.py status

Write-Host ""
Write-Host "[3/3] Choose an option:" -ForegroundColor Green
Write-Host "  1. Launch Web Interface" -ForegroundColor White
Write-Host "  2. Show Data Statistics" -ForegroundColor White
Write-Host "  3. Show AI Insights" -ForegroundColor White
Write-Host "  4. Show D2C Analysis" -ForegroundColor White
Write-Host "  5. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-5)"

switch ($choice) {
    "1" {
        Write-Host "Launching Streamlit web interface..." -ForegroundColor Green
        streamlit run src/ui/streamlit_app.py
    }
    "2" {
        Write-Host "Showing data statistics..." -ForegroundColor Green
        python -c "import pandas as pd; df = pd.read_parquet('data/processed/combined_apps.parquet'); print(f'Total Apps: {len(df):,}'); print(f'Android: {len(df[df[\"platform\"].isin([\"Android\", \"Both\"])]):,}'); print(f'iOS: {len(df[df[\"platform\"].isin([\"iOS\", \"Both\"])]):,}'); print(f'Categories: {df[\"category\"].nunique()}'); print(f'Avg Rating: {df[\"rating\"].mean():.2f}')"
    }
    "3" {
        Write-Host "Showing AI insights..." -ForegroundColor Green
        python show_ai_insights.py
    }
    "4" {
        Write-Host "Showing D2C analysis..." -ForegroundColor Green
        python -c "import json; d2c = json.load(open('artifacts/d2c_metrics.json')); print(f'D2C Analysis: {d2c[\"funnel_metrics\"][\"overall_metrics\"][\"total_campaigns\"]} campaigns, ROAS: {d2c[\"funnel_metrics\"][\"revenue_metrics\"][\"roas\"]:.2f}')"
    }
    "5" {
        Write-Host "Goodbye!" -ForegroundColor Green
        exit
    }
    default {
        Write-Host "Invalid choice. Please run the script again." -ForegroundColor Red
    }
}

Write-Host ""
Read-Host "Press Enter to continue"
