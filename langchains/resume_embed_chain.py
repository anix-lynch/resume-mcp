#!/usr/bin/env python3
"""
Resume Embedding Chain
Embeds resume data using free/cheap embedding models.
Uses sentence-transformers (free, local) as primary, Gemini as fallback.
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Try free options first
try:
    from sentence_transformers import SentenceTransformer
    USE_SENTENCE_TRANSFORMERS = True
    print("✅ Using sentence-transformers (free, local)")
except ImportError:
    USE_SENTENCE_TRANSFORMERS = False
    print("⚠️  sentence-transformers not installed, will use API")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    if os.getenv("GEMINI_API_KEY"):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        print("✅ Gemini API configured (free tier)")
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  Gemini not available")

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    USE_HUGGINGFACE = True
    print("✅ HuggingFace embeddings available (free)")
except ImportError:
    USE_HUGGINGFACE = False

def load_resume(resume_file='resume.json'):
    """Load resume data."""
    resume_path = Path(resume_file)
    if not resume_path.exists():
        print(f"❌ Resume file not found: {resume_file}")
        return None
    
    with open(resume_path, 'r') as f:
        return json.load(f)

def create_resume_text(resume):
    """Create text representation of resume for embedding."""
    parts = []
    
    # Name and title
    if resume.get('name'):
        parts.append(f"Name: {resume['name']}")
    if resume.get('title'):
        parts.append(f"Title: {resume['title']}")
    
    # Skills
    if resume.get('skills'):
        skills_list = []
        for skill, weight in resume['skills'].items():
            skills_list.append(f"{skill}({weight})")
        parts.append(f"Skills: {', '.join(skills_list)}")
    
    # Projects
    if resume.get('projects'):
        parts.append("Projects:")
        for project in resume['projects'][:5]:  # Top 5 projects
            if project.get('name'):
                parts.append(f"- {project['name']}")
            if project.get('description'):
                parts.append(f"  {project['description'][:200]}...")
            if project.get('tech'):
                parts.append(f"  Tech: {', '.join(project['tech'])}")
    
    # Experience
    if resume.get('experience'):
        parts.append("Experience:")
        for exp in resume['experience'][:3]:  # Top 3 experiences
            if exp.get('company') and exp.get('title'):
                parts.append(f"- {exp['title']} at {exp['company']}")
            if exp.get('description'):
                parts.append(f"  {exp['description'][:200]}...")
    
    return "\n".join(parts)

def embed_resume_free(resume_text):
    """Embed resume using free sentence-transformers (local, no API)."""
    if not USE_SENTENCE_TRANSFORMERS:
        return None
    
    # Use a good free model (no API needed!)
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Free, fast, good quality
    embedding = model.encode(resume_text)
    
    print(f"✅ Embedded resume using sentence-transformers (free, local)")
    print(f"   Embedding dimension: {len(embedding)}")
    
    return embedding.tolist()

def embed_resume_gemini(resume_text):
    """Embed resume using Gemini API (free tier)."""
    if not GEMINI_AVAILABLE or not os.getenv("GEMINI_API_KEY"):
        return None
    
    try:
        # Gemini embeddings
        model = genai.GenerativeModel('embedding-001')
        result = model.embed_content(resume_text)
        embedding = result['embedding']
        
        print(f"✅ Embedded resume using Gemini (free tier)")
        print(f"   Embedding dimension: {len(embedding)}")
        
        return embedding
    except Exception as e:
        print(f"⚠️  Gemini embedding failed: {e}")
        return None

def embed_resume(resume_file='resume.json', use_free=True):
    """
    Embed resume using free/cheap options first.
    
    Priority:
    1. sentence-transformers (free, local, no API)
    2. Gemini (free tier)
    3. OpenAI (fallback, expensive)
    """
    resume = load_resume(resume_file)
    if not resume:
        return None
    
    resume_text = create_resume_text(resume)
    print(f"📝 Resume text length: {len(resume_text)} characters")
    
    # Try free options first
    if use_free and USE_SENTENCE_TRANSFORMERS:
        embedding = embed_resume_free(resume_text)
        if embedding:
            return {
                'embedding': embedding,
                'method': 'sentence-transformers',
                'model': 'all-MiniLM-L6-v2',
                'cost': 'FREE (local)'
            }
    
    # Try Gemini (free tier)
    if GEMINI_AVAILABLE:
        embedding = embed_resume_gemini(resume_text)
        if embedding:
            return {
                'embedding': embedding,
                'method': 'gemini',
                'model': 'embedding-001',
                'cost': 'FREE (API)'
            }
    
    # Fallback to OpenAI (expensive)
    print("⚠️  Using OpenAI as fallback (more expensive)")
    try:
        from langchain_openai import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings()
        embedding = embeddings.embed_query(resume_text)
        return {
            'embedding': embedding,
            'method': 'openai',
            'model': 'text-embedding-ada-002',
            'cost': 'PAID'
        }
    except Exception as e:
        print(f"❌ All embedding methods failed: {e}")
        return None

if __name__ == "__main__":
    print("🧠 Testing Resume Embedding (Free Options First)")
    print("=" * 50)
    
    result = embed_resume()
    if result:
        print(f"\n✅ Success!")
        print(f"   Method: {result['method']}")
        print(f"   Model: {result['model']}")
        print(f"   Cost: {result['cost']}")
        print(f"   Embedding size: {len(result['embedding'])}")
    else:
        print("\n❌ Failed to embed resume")

