#!/usr/bin/env python3
"""
Normalize job data from raw/foorila raw.csv
Creates job descriptions from available metadata since CSV doesn't have description column.
"""

import pandas as pd
import json
from pathlib import Path

def normalize_foorila_jobs():
    """Normalize foorila CSV and create job descriptions."""
    
    # Load raw data
    raw_file = Path("raw/foorila raw.csv")
    if not raw_file.exists():
        print(f"❌ File not found: {raw_file}")
        return False
    
    print(f"📂 Loading: {raw_file}")
    df = pd.read_csv(raw_file)
    print(f"✅ Loaded {len(df)} jobs")
    
    # Create job descriptions from available data
    # Since CSV doesn't have description, we'll create one from metadata
    descriptions = []
    for idx, row in df.iterrows():
        desc_parts = []
        
        # Add title
        if pd.notna(row.get('title')):
            desc_parts.append(f"Title: {row['title']}")
        
        # Add company
        if pd.notna(row.get('company')):
            desc_parts.append(f"Company: {row['company']}")
        
        # Add location
        if pd.notna(row.get('location')):
            desc_parts.append(f"Location: {row['location']}")
        
        # Add remote status
        if pd.notna(row.get('has_remote')) and row['has_remote'] == 'Y':
            desc_parts.append("Remote: Yes")
        
        # Add experience level
        if pd.notna(row.get('experience_level')):
            desc_parts.append(f"Experience Level: {row['experience_level']}")
        
        # Add experience years
        if pd.notna(row.get('experience_years')):
            desc_parts.append(f"Experience Required: {row['experience_years']} years")
        
        # Add salary if available
        if pd.notna(row.get('salary_min')) and pd.notna(row.get('salary_max')):
            currency = row.get('salary_currency', 'USD')
            desc_parts.append(f"Salary: {currency} {row['salary_min']}-{row['salary_max']}")
        elif pd.notna(row.get('salary_min')):
            currency = row.get('salary_currency', 'USD')
            desc_parts.append(f"Salary: {currency} {row['salary_min']}+")
        
        # Combine into description
        description = ". ".join(desc_parts)
        descriptions.append(description)
    
    # Add description column
    df['description'] = descriptions
    
    # Normalize column names (lowercase, underscores)
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Ensure required columns exist
    required_cols = ['company', 'title', 'description', 'location']
    for col in required_cols:
        if col not in df.columns:
            df[col] = ''
    
    # Create output directory
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    
    # Save normalized data
    output_file = output_dir / "jobs_normalized.csv"
    df.to_csv(output_file, index=False)
    print(f"✅ Saved normalized jobs to: {output_file}")
    print(f"   Total jobs: {len(df)}")
    print(f"   Columns: {list(df.columns)}")
    
    # Show sample
    print(f"\n📋 Sample job description:")
    print(f"   {descriptions[0][:100]}...")
    
    return True

if __name__ == "__main__":
    normalize_foorila_jobs()

