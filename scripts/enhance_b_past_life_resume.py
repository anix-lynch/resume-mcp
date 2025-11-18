#!/usr/bin/env python3
"""
Comprehensive extraction from CV 2019 docx - extract EVERY detail
"""
import json
import re
from pathlib import Path
from docx import Document

def extract_full_cv_details(docx_path):
    """Extract comprehensive details from CV docx."""
    doc = Document(docx_path)
    
    # Extract all text
    full_text = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            full_text.append(text)
    
    return full_text

def parse_comprehensive_resume(full_text):
    """Parse extracted CV data into comprehensive resume JSON with ALL details."""
    
    text = "\n".join(full_text)
    
    resume = {
        "name": "Anix Lynch",
        "title": "Venture Capital, Managing Partner | PE/VC Investment Professional",
        "contact": {
            "phone": "+66-90-980-1799",
            "email": "anix@chicagobooth.edu",
            "location": "Thailand",
            "skype": "anixlynch",
            "social": "Skype/FB/LINE/WhatsApp: anixlynch"
        },
        "summary": "",
        "skills": {},
        "experience": [],
        "education": [],
        "certifications": [],
        "projects": [],
        "achievements": [],
        "board_positions": [],
        "advisory_roles": [],
        "publications": [],
        "speaking_engagements": [],
        "judging_engagements": [],
        "mentoring_engagements": [],
        "media_appearances": [],
        "awards": [],
        "languages": {},
        "target_roles": [],
        "target_rate_range": {},
        "track_record": {},
        "fun_facts": []
    }
    
    # Extract summary (first paragraph after name)
    for i, line in enumerate(full_text):
        if "Managing Partner at Expara" in line or "over 20 years" in line:
            resume["summary"] = line
            break
    
    # Extract experience with FULL details
    experience_section = False
    current_exp = {}
    
    for i, line in enumerate(full_text):
        line_clean = line.strip()
        
        # Start of experience section
        if "EXPERIENCE" in line_clean:
            experience_section = True
            continue
        
        if not experience_section:
            continue
        
        # End of experience section
        if "EDUCATION" in line_clean:
            if current_exp:
                resume["experience"].append(current_exp)
            break
        
        # Detect new experience entry (company name pattern)
        if any(keyword in line_clean for keyword in ["Managing Partner", "CEO", "VP", "General Manager", "Asset Manager", "Investment Associate", "Manager", "Strategic Planning"]):
            # Save previous experience
            if current_exp and current_exp.get("company"):
                resume["experience"].append(current_exp)
            
            # Start new experience
            current_exp = {
                "company": "",
                "title": "",
                "duration": "",
                "location": "",
                "description": [],
                "achievements": [],
                "metrics": {},
                "keywords": []
            }
            
            # Extract title and company
            parts = line_clean.split(",")
            if len(parts) >= 2:
                current_exp["company"] = parts[0].strip()
                if len(parts) >= 3:
                    current_exp["location"] = parts[1].strip()
                    current_exp["title"] = parts[2].strip()
                else:
                    current_exp["title"] = parts[1].strip()
            else:
                # Try to extract from line
                if "Managing Partner" in line_clean:
                    current_exp["title"] = "Managing Partner"
                    current_exp["company"] = line_clean.split("Managing Partner")[0].strip().rstrip(",")
                elif "CEO" in line_clean:
                    current_exp["title"] = "CEO"
                    current_exp["company"] = line_clean.split("CEO")[0].strip().rstrip(",")
            
            # Look for duration (next line or same line)
            if i + 1 < len(full_text):
                next_line = full_text[i + 1].strip()
                if re.search(r'\d{1,2}/\d{4}', next_line) or "to present" in next_line.lower() or "to " in next_line.lower():
                    current_exp["duration"] = next_line
            
            # Extract duration from current line if present
            duration_match = re.search(r'\d{1,2}/\d{4}\s+to\s+(present|\d{1,2}/\d{4})', line_clean)
            if duration_match:
                current_exp["duration"] = duration_match.group(0)
        
        # Collect description lines for current experience
        elif current_exp and line_clean and len(line_clean) > 20:
            # Skip if it's a section header
            if any(header in line_clean for header in ["Public Speaking:", "Television", "Impact:", "Signature Projects:"]):
                continue
            
            current_exp["description"].append(line_clean)
            
            # Extract metrics (dollar amounts, percentages, numbers)
            dollar_matches = re.findall(r'\$[\d.]+[BMK]?', line_clean)
            if dollar_matches:
                if "metrics" not in current_exp:
                    current_exp["metrics"] = {}
                current_exp["metrics"]["deal_sizes"] = dollar_matches
            
            percent_matches = re.findall(r'\d+%', line_clean)
            if percent_matches:
                if "metrics" not in current_exp:
                    current_exp["metrics"] = {}
                current_exp["metrics"]["percentages"] = percent_matches
    
    # Save last experience
    if current_exp and current_exp.get("company"):
        resume["experience"].append(current_exp)
    
    # Extract speaking engagements
    speaking_section = False
    for i, line in enumerate(full_text):
        if "Public Speaking:" in line:
            speaking_section = True
            continue
        if speaking_section:
            if line.strip() and not line.strip().startswith("Television"):
                if any(keyword in line.lower() for keyword in ["panelist", "keynote", "speaker", "lecturer", "advisor", "judge", "mentor"]):
                    resume["speaking_engagements"].append(line.strip())
            elif "Television" in line:
                break
    
    # Extract judging engagements
    for line in full_text:
        if "Judge" in line and "judging_engagements" not in line.lower():
            resume["judging_engagements"].append(line.strip())
        elif "Mentor" in line and "judging" not in line.lower():
            resume["mentoring_engagements"].append(line.strip())
    
    # Extract media appearances
    media_section = False
    for line in full_text:
        if "Television and Press Conference:" in line:
            media_section = True
            continue
        if media_section:
            if line.strip() and "EDUCATION" not in line:
                resume["media_appearances"].append(line.strip())
            elif "EDUCATION" in line:
                break
    
    # Extract education
    education_section = False
    for line in full_text:
        if "EDUCATION & QUALIFICATIONS" in line:
            education_section = True
            continue
        if education_section:
            if line.strip() and "FUN FACTS" not in line:
                if "MBA:" in line or "BA " in line or "Certificate" in line or "Certified" in line:
                    resume["education"].append(line.strip())
            elif "FUN FACTS" in line:
                break
    
    # Extract fun facts
    fun_facts_section = False
    for line in full_text:
        if "FUN FACTS ABOUT ANIX" in line:
            fun_facts_section = True
            continue
        if fun_facts_section:
            if line.strip():
                resume["fun_facts"].append(line.strip())
    
    # Extract comprehensive skills from entire text
    skill_categories = {
        "Venture Capital": ["venture capital", "vc", "fund", "startup investment", "deal sourcing", "portfolio management"],
        "Private Equity": ["private equity", "pe", "acquisition", "m&a", "due diligence"],
        "Real Estate": ["real estate", "reit", "property", "asset management", "hospitality"],
        "Strategic Planning": ["strategic planning", "policy", "ecosystem", "government relations"],
        "Financial": ["financial modeling", "irr", "fp&a", "cap table", "waterfall"],
        "Leadership": ["managing partner", "ceo", "vp", "team management", "board"],
        "Ecosystem Building": ["ecosystem", "accelerator", "incubator", "community building"],
        "Impact Investing": ["impact investing", "philanthropy", "sustainability", "social entrepreneurship"],
        "Cross-border": ["cross-border", "global", "international", "silicon valley"],
        "Languages": ["japanese", "thai", "english"]
    }
    
    text_lower = text.lower()
    for skill_name, keywords in skill_categories.items():
        mentions = sum(text_lower.count(kw) for kw in keywords)
        if mentions > 0:
            resume["skills"][skill_name] = min(10, 7 + min(mentions, 3))
    
    # Extract track record
    resume["track_record"] = {
        "total_experience": "20+ years",
        "pe_vc_track_record": "$2B+",
        "deals_screened_per_year": "700+",
        "fund_size_managed": "Up to $1M check size",
        "successful_exits": ["2C2P", "Co-asset"],
        "portfolio_companies": ["Ooca", "Event Banana", "Peak Engine", "One Stockhome"],
        "team_managed": "3 FTE associates, 6 vendors, 2 LPs, 8 accelerators, 40+ VCs, 6 media partners",
        "deals_closed": "Multiple",
        "avg_deal_size_mqdc": "$500M",
        "irr_achieved": "25%+ (MGPA BlackRock), 22%+ (New City Corporation)",
        "equity_multiple": "2x (MGPA BlackRock)"
    }
    
    # Extract projects with full details
    projects_text = text
    
    # Expara projects
    if "Techsauce FAB" in projects_text:
        resume["projects"].append({
            "name": "Techsauce FAB (Food/Agri/Biotech)",
            "description": "Created flagship program discussing future-forward topics. Built 15 stages covering Genome Editing, CRISPR food, Food Blockchain, Menu of 2030, 3D Printing - Organ on Demand, BioHacking, Social Dilemma in BioTech. Key speakers: Indiebio, Agfunder, SproutX, Top Ittipat (Taokaenoi). Helped grow audience from 10,000 to 15,000. Currently building community of 500 startups.",
            "tech": ["Ecosystem Building", "Event Management", "Community Building", "Biotech", "AgTech", "FoodTech"],
            "weight": 10,
            "metrics": {
                "stages": 15,
                "audience_growth": "10,000 to 15,000",
                "startup_community": "500 startups"
            }
        })
    
    if "Bangkok Beta" in projects_text or "Thailand 4.0" in projects_text:
        resume["projects"].append({
            "name": "Bangkok Beta / Thailand 4.0",
            "description": "Initiated and proposed innovative country plan to Ministry of ICT/Ministry of Science and True Telecom. Synthetized Call-To-Action Formula identifying incentives/obstacles for ecosystem participants. 17+ out of 26 suggestions implemented in Thai startup economy. Estimated GDP impact: $395M+ budget to produce 1-5 tech unicorns in 8 years.",
            "tech": ["Policy Consulting", "Strategic Planning", "Government Relations", "Ecosystem Development"],
            "weight": 10,
            "metrics": {
                "suggestions_implemented": "17+ out of 26",
                "budget_estimated": "$395M+",
                "impact": "Thailand's Ease of Doing Business improved by 3 points (World Bank)"
            }
        })
    
    if "True Digital Park" in projects_text:
        resume["projects"].append({
            "name": "True Digital Park",
            "description": "Originated 1st draft concept. Successfully drove JV between MQDC/True, USD$568M, 10,000 Sqm. Successfully launched in 2018. Recognized by True Corporation as 'Tech ecosystem alliance'.",
            "tech": ["Real Estate", "JV Development", "Concept Innovation", "Ecosystem Building"],
            "weight": 10,
            "metrics": {
                "deal_size": "$568M",
                "size": "10,000 Sqm",
                "launch_year": "2018"
            }
        })
    
    if "Whizdom101" in projects_text:
        resume["projects"].append({
            "name": "Whizdom101",
            "description": "Thailand's largest mixed-use development with Virgin Group (USD$1.5B). Features vertical sport club and smart home. Lease 50%+, Sold over 80%.",
            "tech": ["Real Estate Development", "Mixed-use", "Partnership Development", "Smart Home"],
            "weight": 9,
            "metrics": {
                "deal_size": "$1.5B",
                "lease_rate": "50%+",
                "sales_rate": "80%+"
            }
        })
    
    # Extract target roles
    resume["target_roles"] = [
        "Venture Capital Partner",
        "Private Equity Principal",
        "Fund Manager",
        "Investment Director",
        "Startup Ecosystem Builder",
        "Strategic Advisor",
        "Real Estate Investment Manager",
        "Policy Consultant",
        "Board Member",
        "CVC Head"
    ]
    
    # Extract languages
    resume["languages"] = {
        "Japanese": 10,
        "Thai": 9,
        "English": 10
    }
    
    # Extract awards
    resume["awards"] = [
        "Thailand's Top Female VCs",
        "Short Documentary Producer Award Winner (Silver), World MBA council, 2012, France",
        "Hidden Talent Award, 2012",
        "Recognized by Princess Sirinthorn on TV (2011)"
    ]
    
    # Extract target rate
    resume["target_rate_range"] = {
        "min": 150,
        "max": 500,
        "currency": "USD",
        "unit": "hour"
    }
    
    # Clean up experience descriptions
    for exp in resume["experience"]:
        if exp.get("description"):
            exp["full_description"] = "\n".join(exp["description"])
            # Extract keywords from description
            exp["keywords"] = extract_keywords_from_text("\n".join(exp["description"]))
    
    return resume

def extract_keywords_from_text(text):
    """Extract relevant keywords from text."""
    keywords = []
    skill_keywords = [
        "venture capital", "private equity", "fund", "deal", "portfolio",
        "startup", "real estate", "m&a", "strategic", "due diligence",
        "financial", "ecosystem", "government", "impact", "reit", "ipo",
        "acquisition", "investment", "sourcing", "exits", "irr", "equity multiple"
    ]
    for kw in skill_keywords:
        if kw in text.lower():
            keywords.append(kw.title())
    return list(set(keywords))

if __name__ == "__main__":
    docx_path = Path("Anix Lynch CV 2019 for paulina.docx")
    
    print("📄 Extracting comprehensive CV details...")
    full_text = extract_full_cv_details(docx_path)
    
    print(f"✅ Extracted {len(full_text)} paragraphs")
    
    print("\n📝 Parsing to comprehensive resume...")
    enhanced_resume = parse_comprehensive_resume(full_text)
    
    # Save enhanced resume
    output_path = Path("b_past_life_mcp/resume.json")
    with open(output_path, 'w') as f:
        json.dump(enhanced_resume, f, indent=2)
    
    print(f"✅ Comprehensive resume saved to {output_path}")
    print(f"\n📊 Summary:")
    print(f"   - Experience entries: {len(enhanced_resume['experience'])}")
    print(f"   - Skills: {len(enhanced_resume['skills'])}")
    print(f"   - Projects: {len(enhanced_resume['projects'])}")
    print(f"   - Speaking engagements: {len(enhanced_resume['speaking_engagements'])}")
    print(f"   - Judging engagements: {len(enhanced_resume['judging_engagements'])}")
    print(f"   - Media appearances: {len(enhanced_resume['media_appearances'])}")
    print(f"   - Education: {len(enhanced_resume['education'])}")
    print(f"   - Fun facts: {len(enhanced_resume['fun_facts'])}")
