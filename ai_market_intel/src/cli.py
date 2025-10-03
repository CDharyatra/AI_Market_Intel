#!/usr/bin/env python3
"""
Command Line Interface for AI Market Intelligence
Provides CLI access to key functionality.
"""

import argparse
import sys
import os
import json
from pathlib import Path

def generate_insights():
    """Generate insights from the pipeline."""
    print("Generating AI insights...")
    
    # Check if aggregates exist
    aggregates_path = "artifacts/aggregates.json"
    if not Path(aggregates_path).exists():
        print("Error: Aggregates not found. Please run the pipeline first.")
        return False
    
    # Run insights generation
    cmd = f"python src/insights/generate_insights.py --input {aggregates_path} --out artifacts/insights.json"
    result = os.system(cmd)
    
    if result == 0:
        print("Insights generated successfully!")
        
        # Load and display summary
        with open("artifacts/insights.json", 'r') as f:
            insights = json.load(f)
        
        print(f"\nGenerated {len(insights['insights'])} insights:")
        for i, insight in enumerate(insights['insights'], 1):
            print(f"{i}. {insight['title']} (Confidence: {insight['confidence']:.0%})")
        
        return True
    else:
        print("Error generating insights")
        return False

def generate_report():
    """Generate executive report."""
    print("Generating executive report...")
    
    # Check if insights exist
    insights_path = "artifacts/insights.json"
    if not Path(insights_path).exists():
        print("Error: Insights not found. Please generate insights first.")
        return False
    
    # Run report generation
    cmd = f"python src/reports/generate_report.py --insights {insights_path} --out artifacts/report.pdf"
    result = os.system(cmd)
    
    if result == 0:
        print("Executive report generated successfully!")
        print("Report saved to: artifacts/report.pdf")
        return True
    else:
        print("Error generating report")
        return False

def run_full_pipeline():
    """Run the complete data pipeline."""
    print("Running full AI Market Intelligence pipeline...")
    
    steps = [
        ("Computing aggregates", "python src/insights/compute_aggregates.py"),
        ("Generating insights", "python src/insights/generate_insights.py --input artifacts/aggregates.json --out artifacts/insights.json"),
        ("Enriching insights", "python src/insights/enrich_insights.py --insights artifacts/insights.json --out artifacts/insights.json"),
        ("Generating report", "python src/reports/generate_report.py --insights artifacts/insights.json --out artifacts/report.pdf")
    ]
    
    for step_name, cmd in steps:
        print(f"\n{step_name}...")
        result = os.system(cmd)
        if result != 0:
            print(f"Error in {step_name}")
            return False
    
    print("\nFull pipeline completed successfully!")
    return True

def show_status():
    """Show pipeline status and available artifacts."""
    print("AI Market Intelligence Pipeline Status")
    print("=" * 40)
    
    artifacts_dir = Path("artifacts")
    data_dir = Path("data")
    
    # Check data files
    print("\nData Files:")
    data_files = [
        ("Raw Android Data", "data/raw/kaggle_google_play.parquet"),
        ("Raw iOS Data", "data/raw/rapidapi_appstore.jsonl"),
        ("Cleaned Android Data", "data/processed/kaggle_cleaned.parquet"),
        ("Cleaned iOS Data", "data/processed/rapidapi_ios.parquet"),
        ("Combined Dataset", "data/processed/combined_apps.parquet")
    ]
    
    for name, path in data_files:
        exists = Path(path).exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {name}: {path}")
    
    # Check artifacts
    print("\nArtifacts:")
    artifact_files = [
        ("Statistical Aggregates", "artifacts/aggregates.json"),
        ("AI Insights", "artifacts/insights.json"),
        ("Executive Report", "artifacts/report.pdf"),
        ("Name Matches", "artifacts/name_matches.csv")
    ]
    
    for name, path in artifact_files:
        exists = Path(path).exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {name}: {path}")
    
    # Check charts
    charts_dir = Path("artifacts/charts")
    if charts_dir.exists():
        chart_files = list(charts_dir.glob("*.png"))
        print(f"\nCharts: {len(chart_files)} files in artifacts/charts/")
        for chart in chart_files:
            print(f"  • {chart.name}")
    
    # Load and display insights summary if available
    insights_path = "artifacts/insights.json"
    if Path(insights_path).exists():
        try:
            with open(insights_path, 'r') as f:
                insights = json.load(f)
            
            print(f"\nInsights Summary:")
            print(f"  Total insights: {len(insights['insights'])}")
            avg_confidence = sum(i['confidence'] for i in insights['insights']) / len(insights['insights'])
            print(f"  Average confidence: {avg_confidence:.0%}")
            
            if 'key_trends' in insights:
                print(f"  Key trends: {len(insights['key_trends'])}")
        except:
            pass

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='AI Market Intelligence CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/cli.py generate_insights    # Generate AI insights
  python src/cli.py generate_report      # Generate executive report
  python src/cli.py run_pipeline         # Run full pipeline
  python src/cli.py status               # Show pipeline status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate insights command
    subparsers.add_parser('generate_insights', help='Generate AI insights from data')
    
    # Generate report command
    subparsers.add_parser('generate_report', help='Generate executive report')
    
    # Run pipeline command
    subparsers.add_parser('run_pipeline', help='Run the complete data pipeline')
    
    # Status command
    subparsers.add_parser('status', help='Show pipeline status and artifacts')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Change to project directory
    os.chdir(Path(__file__).parent.parent)
    
    # Execute command
    if args.command == 'generate_insights':
        success = generate_insights()
    elif args.command == 'generate_report':
        success = generate_report()
    elif args.command == 'run_pipeline':
        success = run_full_pipeline()
    elif args.command == 'status':
        show_status()
        success = True
    else:
        print(f"Unknown command: {args.command}")
        success = False
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
