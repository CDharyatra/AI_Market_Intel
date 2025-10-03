#!/usr/bin/env python3
"""
Executive Report Generation Script
Generates a comprehensive PDF report from insights and data.
"""

import json
import argparse
import os
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import pandas as pd
from datetime import datetime

def load_insights(filepath):
    """Load insights from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def load_aggregates(filepath):
    """Load aggregates from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def create_title_page(doc, styles):
    """Create the title page of the report."""
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    story.append(Paragraph("AI Market Intelligence Report", title_style))
    story.append(Spacer(1, 20))
    
    # Subtitle
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    
    story.append(Paragraph("Mobile App Store Analysis & Insights", subtitle_style))
    story.append(Spacer(1, 40))
    
    # Date
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", date_style))
    story.append(PageBreak())
    
    return story

def create_executive_summary(insights, story, styles):
    """Create executive summary section."""
    story.append(Paragraph("Executive Summary", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    summary_text = insights.get('summary', 'No summary available.')
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Key trends
    if 'key_trends' in insights:
        story.append(Paragraph("Key Market Trends:", styles['Heading2']))
        story.append(Spacer(1, 6))
        
        for trend in insights['key_trends']:
            story.append(Paragraph(f"• {trend}", styles['Normal']))
            story.append(Spacer(1, 3))
    
    story.append(Spacer(1, 20))

def create_insights_section(insights, story, styles):
    """Create detailed insights section."""
    story.append(Paragraph("Detailed Market Insights", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    for i, insight in enumerate(insights['insights'], 1):
        # Insight title
        title_style = ParagraphStyle(
            'InsightTitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=6,
            textColor=colors.darkblue
        )
        
        story.append(Paragraph(f"{i}. {insight['title']}", title_style))
        
        # Description
        story.append(Paragraph(insight['description'], styles['Normal']))
        story.append(Spacer(1, 6))
        
        # Confidence and category
        confidence_text = f"<b>Confidence:</b> {insight['confidence']:.0%} | <b>Category:</b> {insight['category']}"
        story.append(Paragraph(confidence_text, styles['Normal']))
        story.append(Spacer(1, 6))
        
        # Supporting data
        if 'supporting_data' in insight and insight['supporting_data']:
            story.append(Paragraph("<b>Supporting Data:</b>", styles['Normal']))
            for key, value in insight['supporting_data'].items():
                if isinstance(value, (int, float)):
                    story.append(Paragraph(f"• {key.replace('_', ' ').title()}: {value:,.2f}", styles['Normal']))
                else:
                    story.append(Paragraph(f"• {key.replace('_', ' ').title()}: {value}", styles['Normal']))
            story.append(Spacer(1, 6))
        
        # Implications
        if 'implications' in insight:
            story.append(Paragraph("<b>Implications:</b>", styles['Normal']))
            story.append(Paragraph(insight['implications'], styles['Normal']))
            story.append(Spacer(1, 6))
        
        # Recommendations
        if 'recommendations' in insight:
            story.append(Paragraph("<b>Recommendations:</b>", styles['Normal']))
            story.append(Paragraph(insight['recommendations'], styles['Normal']))
        
        story.append(Spacer(1, 20))

def create_data_overview(aggregates, story, styles):
    """Create data overview section."""
    story.append(Paragraph("Data Overview", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    overall = aggregates['overall_stats']
    
    # Create overview table
    data = [
        ['Metric', 'Value'],
        ['Total Apps Analyzed', f"{overall['total_apps']:,}"],
        ['Categories', f"{overall['total_categories']}"],
        ['Average Rating', f"{overall['avg_rating']:.2f}"],
        ['Paid Apps', f"{overall['paid_apps']:,} ({overall['paid_apps']/overall['total_apps']*100:.1f}%)"],
        ['Free Apps', f"{overall['free_apps']:,} ({overall['free_apps']/overall['total_apps']*100:.1f}%)"],
        ['Average Price (Paid)', f"${overall['avg_price']:.2f}"],
        ['Cross-Platform Apps', f"{aggregates['cross_platform_insights'].get('total_cross_platform_apps', 0):,}"]
    ]
    
    table = Table(data, colWidths=[2.5*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Platform distribution
    story.append(Paragraph("Platform Distribution", styles['Heading2']))
    story.append(Spacer(1, 6))
    
    platform_data = []
    for platform, stats in aggregates['platform_stats'].items():
        platform_data.append([
            platform,
            f"{stats['total_apps']:,}",
            f"{stats['avg_rating']:.2f}",
            f"{stats['paid_apps']:,}"
        ])
    
    platform_table = Table(
        [['Platform', 'Apps', 'Avg Rating', 'Paid Apps']] + platform_data,
        colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch]
    )
    platform_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(platform_table)
    story.append(Spacer(1, 20))

def add_charts_to_report(insights, story, styles):
    """Add chart references to the report."""
    if 'available_charts' in insights and insights['available_charts']:
        story.append(Paragraph("Supporting Visualizations", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("The following charts support the insights presented in this report:", styles['Normal']))
        story.append(Spacer(1, 6))
        
        chart_descriptions = insights.get('chart_descriptions', {})
        for chart_file in insights['available_charts']:
            description = chart_descriptions.get(chart_file, chart_file)
            story.append(Paragraph(f"• {description}", styles['Normal']))
        
        story.append(Spacer(1, 20))

def main():
    """Main function to generate the report."""
    parser = argparse.ArgumentParser(description='Generate executive report from insights')
    parser.add_argument('--insights', required=True, help='Input insights JSON file')
    parser.add_argument('--out', required=True, help='Output PDF file')
    
    args = parser.parse_args()
    
    try:
        # Load data
        print(f"Loading insights from {args.insights}...")
        insights = load_insights(args.insights)
        
        # Load aggregates for additional data
        aggregates_path = "artifacts/aggregates.json"
        if Path(aggregates_path).exists():
            aggregates = load_aggregates(aggregates_path)
        else:
            print("Warning: Aggregates file not found, using limited data")
            aggregates = {'overall_stats': {}, 'platform_stats': {}, 'cross_platform_insights': {}}
        
        # Create PDF document
        print(f"Generating PDF report: {args.out}")
        doc = SimpleDocTemplate(args.out, pagesize=A4)
        styles = getSampleStyleSheet()
        
        # Build story
        story = []
        
        # Title page
        story.extend(create_title_page(doc, styles))
        
        # Executive summary
        create_executive_summary(insights, story, styles)
        
        # Data overview
        create_data_overview(aggregates, story, styles)
        
        # Detailed insights
        create_insights_section(insights, story, styles)
        
        # Charts section
        add_charts_to_report(insights, story, styles)
        
        # Build PDF
        doc.build(story)
        
        print("Executive report generation completed successfully!")
        print(f"Report saved to: {args.out}")
        
        return True
        
    except Exception as e:
        print(f"Error generating report: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
