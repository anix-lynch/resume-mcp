#!/usr/bin/env python3
"""
ETL Clean - Basic deduplication and cleanup for job postings.

Reads jobs_raw.csv, deduplicates by URL, normalizes data,
and outputs jobs_clean.csv.
"""

import pandas as pd
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def normalize_text(text):
    """Normalize text: strip whitespace, lowercase for comparison."""
    if pd.isna(text):
        return ""
    return str(text).strip()

def normalize_company(company):
    """Normalize company names."""
    if pd.isna(company):
        return ""
    company = str(company).strip()
    # Remove common suffixes for deduplication
    suffixes = [' Inc', ' Inc.', ' LLC', ' Corp', ' Corp.', ' Ltd', ' Ltd.']
    for suffix in suffixes:
        if company.endswith(suffix):
            company = company[:-len(suffix)]
    return company.strip()

def clean_jobs(input_file='jobs_raw.csv', output_file='jobs_clean.csv'):
    """
    Clean and deduplicate job postings.
    
    Args:
        input_file: Path to raw jobs CSV
        output_file: Path to output cleaned CSV
    """
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    # Check if input exists
    if not input_path.exists():
        logger.error(f"Input file not found: {input_file}")
        return False
    
    logger.info(f"Reading {input_file}...")
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        return False
    
    # Validate required columns
    required_cols = ['title', 'company', 'url']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing required columns: {missing_cols}")
        return False
    
    initial_count = len(df)
    logger.info(f"Loaded {initial_count} jobs")
    
    # Normalize data
    logger.info("Normalizing data...")
    df['title'] = df['title'].apply(normalize_text)
    df['company'] = df['company'].apply(normalize_company)
    df['url'] = df['url'].apply(normalize_text)
    if 'source' in df.columns:
        df['source'] = df['source'].apply(normalize_text)
    
    # Remove rows with empty required fields
    before_empty_check = len(df)
    df = df[df['title'].str.len() > 0]
    df = df[df['company'].str.len() > 0]
    df = df[df['url'].str.len() > 0]
    removed_empty = before_empty_check - len(df)
    if removed_empty > 0:
        logger.warning(f"Removed {removed_empty} rows with empty required fields")
    
    # Deduplicate by URL (most reliable unique identifier)
    before_dedup = len(df)
    df = df.drop_duplicates(subset=['url'], keep='first')
    duplicates_removed = before_dedup - len(df)
    if duplicates_removed > 0:
        logger.info(f"Removed {duplicates_removed} duplicate URLs")
    
    # Additional deduplication: same title + company
    before_title_dedup = len(df)
    df = df.drop_duplicates(subset=['title', 'company'], keep='first')
    title_duplicates_removed = before_title_dedup - len(df)
    if title_duplicates_removed > 0:
        logger.info(f"Removed {title_duplicates_removed} duplicate title+company combinations")
    
    # Reset index
    df = df.reset_index(drop=True)
    
    final_count = len(df)
    logger.info(f"Cleaned: {initial_count} → {final_count} jobs ({initial_count - final_count} removed)")
    
    # Write output
    logger.info(f"Writing {output_file}...")
    try:
        df.to_csv(output_path, index=False)
        logger.info(f"✓ Successfully wrote {final_count} jobs to {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error writing CSV: {e}")
        return False

if __name__ == '__main__':
    import sys
    
    # Allow custom input/output files
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'jobs_raw.csv'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'jobs_clean.csv'
    
    success = clean_jobs(input_file, output_file)
    sys.exit(0 if success else 1)

