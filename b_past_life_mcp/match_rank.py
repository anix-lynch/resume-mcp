#!/usr/bin/env python3
"""
Match & Rank - Core ranking logic for job matching.

Loads resume.json and rulebook.yaml, filters jobs,
scores each job, and outputs shortlist.csv + discard.csv.
"""

import pandas as pd
import json
import yaml
import logging
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_resume(resume_file='resume.json'):
    """Load resume data from JSON."""
    resume_path = Path(resume_file)
    if not resume_path.exists():
        logger.error(f"Resume file not found: {resume_file}")
        return None
    
    with open(resume_path, 'r') as f:
        return json.load(f)

def load_rulebook(rulebook_file='rulebook.yaml'):
    """Load rulebook from YAML."""
    rulebook_path = Path(rulebook_file)
    if not rulebook_path.exists():
        logger.error(f"Rulebook file not found: {rulebook_file}")
        return None
    
    with open(rulebook_path, 'r') as f:
        return yaml.safe_load(f)

def extract_keywords(text):
    """Extract keywords from text (lowercase, alphanumeric)."""
    if pd.isna(text):
        return []
    text = str(text).lower()
    # Extract words (alphanumeric + hyphens)
    words = re.findall(r'\b[a-z0-9-]+\b', text)
    return words

def count_keyword_matches(text, keywords):
    """Count how many keywords appear in text."""
    if pd.isna(text):
        return 0
    
    text_lower = str(text).lower()
    matches = 0
    matched_keywords = []
    
    for keyword in keywords:
        keyword_lower = keyword.lower()
        # Check for exact word match or phrase match
        if keyword_lower in text_lower:
            matches += 1
            matched_keywords.append(keyword)
    
    return matches, matched_keywords

def calculate_skill_score(job_text, resume_skills):
    """
    Calculate skill match score based on resume skills.
    
    Returns: (score, matched_skills)
    """
    job_keywords = extract_keywords(job_text)
    matched_skills = []
    total_weight = 0
    matched_weight = 0
    
    for skill, weight in resume_skills.items():
        total_weight += weight
        skill_lower = skill.lower()
        
        # Check if skill appears in job text
        if skill_lower in job_text.lower():
            matched_skills.append(skill)
            matched_weight += weight
    
    # Score is percentage of weighted skills matched
    if total_weight == 0:
        return 0, []
    
    score = (matched_weight / total_weight) * 100
    return score, matched_skills

def calculate_project_score(job_text, resume_projects):
    """
    Calculate project match score based on resume projects.
    
    Returns: (score, matched_projects)
    """
    job_text_lower = job_text.lower()
    matched_projects = []
    total_weight = 0
    matched_weight = 0
    
    for project in resume_projects:
        weight = project.get('weight', 5)
        total_weight += weight
        
        # Check project name
        if project['name'].lower() in job_text_lower:
            matched_projects.append(project['name'])
            matched_weight += weight
            continue
        
        # Check tech stack
        for tech in project.get('tech', []):
            if tech.lower() in job_text_lower:
                matched_projects.append(project['name'])
                matched_weight += weight
                break
    
    if total_weight == 0:
        return 0, []
    
    score = (matched_weight / total_weight) * 100
    return score, matched_projects

def filter_jobs(df, rulebook):
    """
    Filter jobs using positive/negative keywords.
    
    Returns: (filtered_df, discarded_df)
    """
    positive_keywords = rulebook.get('positive_keywords', [])
    negative_keywords = rulebook.get('negative_keywords', [])
    min_positive = rulebook.get('min_positive_matches', 1)
    max_negative = rulebook.get('max_negative_matches', 0)
    
    filtered_indices = []
    discarded_indices = []
    discard_reasons = []
    
    for idx, row in df.iterrows():
        # Combine title and company for keyword matching
        job_text = f"{row['title']} {row.get('company', '')}".lower()
        
        # Check positive keywords
        positive_matches = sum(1 for kw in positive_keywords if kw.lower() in job_text)
        
        # Check negative keywords
        negative_matches = sum(1 for kw in negative_keywords if kw.lower() in job_text)
        
        # Apply filters
        if positive_matches >= min_positive and negative_matches <= max_negative:
            filtered_indices.append(idx)
        else:
            discarded_indices.append(idx)
            reason = []
            if positive_matches < min_positive:
                reason.append(f"insufficient positive matches ({positive_matches} < {min_positive})")
            if negative_matches > max_negative:
                reason.append(f"negative keyword matches ({negative_matches} > {max_negative})")
            discard_reasons.append("; ".join(reason))
    
    filtered_df = df.loc[filtered_indices].copy()
    discarded_df = df.loc[discarded_indices].copy()
    discarded_df['discard_reason'] = discard_reasons
    
    return filtered_df, discarded_df

def rank_jobs(df, resume, rulebook):
    """
    Rank jobs by match score.
    
    Returns: DataFrame with match_score, matched_skills, matched_projects columns
    """
    results = []
    
    for idx, row in df.iterrows():
        # Combine all text fields for matching
        job_text = f"{row['title']} {row.get('company', '')} {row.get('description', '')}"
        
        # Calculate scores
        skill_score, matched_skills = calculate_skill_score(job_text, resume['skills'])
        project_score, matched_projects = calculate_project_score(job_text, resume['projects'])
        
        # Combined score (weighted average)
        combined_score = (skill_score * 0.6) + (project_score * 0.4)
        
        # Count positive keyword matches (bonus)
        positive_keywords = rulebook.get('positive_keywords', [])
        positive_matches, matched_pos_keywords = count_keyword_matches(job_text, positive_keywords)
        keyword_bonus = min(positive_matches * 2, 10)  # Max 10 point bonus
        
        final_score = combined_score + keyword_bonus
        
        results.append({
            'match_score': round(final_score, 2),
            'matched_skills': ', '.join(matched_skills[:5]),  # Top 5
            'matched_projects': ', '.join(matched_projects[:3]),  # Top 3
            'positive_keyword_matches': positive_matches
        })
    
    # Add results to dataframe
    for col in ['match_score', 'matched_skills', 'matched_projects', 'positive_keyword_matches']:
        df[col] = [r[col] for r in results]
    
    # Sort by match score descending
    df = df.sort_values('match_score', ascending=False)
    
    return df

def match_and_rank(
    jobs_file='jobs_clean.csv',
    resume_file='resume.json',
    rulebook_file='rulebook.yaml',
    shortlist_file='shortlist.csv',
    discard_file='discard.csv',
    top_n=5
):
    """
    Main matching and ranking function.
    """
    # Load data
    logger.info(f"Loading jobs from {jobs_file}...")
    if not Path(jobs_file).exists():
        logger.error(f"Jobs file not found: {jobs_file}")
        logger.info("Run etl_clean.py first to generate jobs_clean.csv")
        return False
    
    df = pd.read_csv(jobs_file)
    logger.info(f"Loaded {len(df)} jobs")
    
    logger.info(f"Loading resume from {resume_file}...")
    resume = load_resume(resume_file)
    if not resume:
        return False
    
    logger.info(f"Loading rulebook from {rulebook_file}...")
    rulebook = load_rulebook(rulebook_file)
    if not rulebook:
        return False
    
    # Filter jobs
    logger.info("Filtering jobs using rulebook...")
    filtered_df, discarded_df = filter_jobs(df, rulebook)
    logger.info(f"Filtered: {len(filtered_df)} passed, {len(discarded_df)} discarded")
    
    # Rank filtered jobs
    logger.info("Ranking jobs...")
    ranked_df = rank_jobs(filtered_df, resume, rulebook)
    
    # Get top N
    shortlist_df = ranked_df.head(top_n).copy()
    logger.info(f"Top {top_n} jobs selected for shortlist")
    
    # Save outputs
    logger.info(f"Writing shortlist to {shortlist_file}...")
    shortlist_df.to_csv(shortlist_file, index=False)
    
    logger.info(f"Writing discarded jobs to {discard_file}...")
    discarded_df.to_csv(discard_file, index=False)
    
    logger.info("✓ Matching and ranking complete!")
    return True, shortlist_df, ranked_df

def print_preview(shortlist_df):
    """Print a pretty preview table of top matches."""
    print("\n" + "="*80)
    print("TOP JOB MATCHES")
    print("="*80)
    
    for idx, row in shortlist_df.iterrows():
        print(f"\n[{idx + 1}] {row['title']}")
        print(f"    Company: {row['company']}")
        print(f"    Match Score: {row['match_score']:.1f}/100")
        print(f"    Matched Skills: {row['matched_skills']}")
        if row.get('matched_projects'):
            print(f"    Matched Projects: {row['matched_projects']}")
        print(f"    URL: {row['url']}")
        print("-" * 80)
    
    print(f"\n✓ Showing top {len(shortlist_df)} matches")
    print("="*80 + "\n")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Match and rank jobs against resume')
    parser.add_argument('--preview', action='store_true', help='Print preview table')
    parser.add_argument('--top-n', type=int, default=5, help='Number of top jobs (default: 5)')
    args = parser.parse_args()
    
    result = match_and_rank(top_n=args.top_n)
    
    if isinstance(result, tuple):
        success, shortlist_df, ranked_df = result
    else:
        success = result
        shortlist_df = None
    
    if success and args.preview and shortlist_df is not None:
        print_preview(shortlist_df)
    
    sys.exit(0 if success else 1)

