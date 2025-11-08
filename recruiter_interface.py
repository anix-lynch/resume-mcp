#!/usr/bin/env python3
"""
Recruiter-Friendly Web Interface for Resume MCP
Allows recruiters to query your resume via web interface
"""
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json
import sys

# Import MCP functions
sys.path.insert(0, str(Path(__file__).parent))
from match_rank import load_resume

app = FastAPI(title="Anix Lynch - Resume API")

def load_resume_data():
    """Load resume data."""
    resume = load_resume()
    return resume

@app.get("/", response_class=HTMLResponse)
async def home():
    """Home page with resume query interface."""
    resume = load_resume_data()
    if not resume:
        return HTMLResponse("<h1>Resume not found</h1>", status_code=404)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{resume.get('name', 'Resume')} - Interactive Resume</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .header p {{
                font-size: 1.2em;
                opacity: 0.9;
            }}
            .content {{
                padding: 40px;
            }}
            .query-section {{
                margin-bottom: 30px;
            }}
            .query-section h2 {{
                color: #333;
                margin-bottom: 20px;
                font-size: 1.5em;
            }}
            .query-buttons {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }}
            button {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 25px;
                border-radius: 10px;
                font-size: 1em;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }}
            .result {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
                display: none;
            }}
            .result.show {{
                display: block;
            }}
            .result pre {{
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                font-size: 0.9em;
            }}
            .loading {{
                text-align: center;
                padding: 20px;
                color: #667eea;
            }}
            .info-section {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin-top: 30px;
            }}
            .info-section h3 {{
                color: #333;
                margin-bottom: 15px;
            }}
            .info-section ul {{
                list-style: none;
                padding-left: 0;
            }}
            .info-section li {{
                padding: 8px 0;
                border-bottom: 1px solid #e0e0e0;
            }}
            .info-section li:last-child {{
                border-bottom: none;
            }}
            .badge {{
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 0.8em;
                margin: 5px 5px 5px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{resume.get('name', 'Resume')}</h1>
                <p>{resume.get('title', 'Professional Profile')}</p>
            </div>
            <div class="content">
                <div class="query-section">
                    <h2>🔍 Query Resume</h2>
                    <p style="margin-bottom: 20px; color: #666;">
                        Ask questions about skills, experience, projects, or check job matches.
                    </p>
                    <div class="query-buttons">
                        <button onclick="queryResume('get_resume_info')">📄 Full Resume</button>
                        <button onclick="queryResume('get_skills')">💼 Skills</button>
                        <button onclick="queryResume('get_shortlist')">⭐ Top Jobs</button>
                        <button onclick="checkJobMatch()">🎯 Check Job Match</button>
                    </div>
                    <div id="result" class="result"></div>
                </div>
                
                <div class="info-section">
                    <h3>📋 Quick Info</h3>
                    <ul>
                        <li><strong>Name:</strong> {resume.get('name', 'N/A')}</li>
                        <li><strong>Title:</strong> {resume.get('title', 'N/A')}</li>
                        <li><strong>Skills:</strong> {', '.join(list(resume.get('skills', {}).keys())[:5])}...</li>
                        <li><strong>Target Roles:</strong> {', '.join(resume.get('target_roles', [])[:3])}...</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <script>
            async function queryResume(endpoint) {{
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = '<div class="loading">⏳ Loading...</div>';
                resultDiv.classList.add('show');
                
                try {{
                    let url = `/api/${{endpoint}}`;
                    if (endpoint === 'get_skills') {{
                        url += '?min_weight=7';
                    }}
                    
                    const response = await fetch(url);
                    const data = await response.json();
                    
                    resultDiv.innerHTML = `
                        <h3>Result:</h3>
                        <pre>${{JSON.stringify(data, null, 2)}}</pre>
                    `;
                }} catch (error) {{
                    resultDiv.innerHTML = `
                        <h3>Error:</h3>
                        <pre>${{error.message}}</pre>
                    `;
                }}
            }}
            
            async function checkJobMatch() {{
                const jobTitle = prompt('Enter job title:');
                if (!jobTitle) return;
                
                const jobDesc = prompt('Enter job description:');
                if (!jobDesc) return;
                
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = '<div class="loading">⏳ Checking match...</div>';
                resultDiv.classList.add('show');
                
                try {{
                    const response = await fetch('/api/check_job_match', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            job_title: jobTitle,
                            job_description: jobDesc
                        }})
                    }});
                    const data = await response.json();
                    
                    resultDiv.innerHTML = `
                        <h3>Job Match Result:</h3>
                        <pre>${{JSON.stringify(data, null, 2)}}</pre>
                    `;
                }} catch (error) {{
                    resultDiv.innerHTML = `
                        <h3>Error:</h3>
                        <pre>${{error.message}}</pre>
                    `;
                }}
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html)

@app.get("/api/get_resume_info")
async def api_get_resume_info():
    """API endpoint for full resume."""
    resume = load_resume_data()
    if not resume:
        return JSONResponse({"error": "Resume not found"}, status_code=404)
    return JSONResponse(resume)

@app.get("/api/get_skills")
async def api_get_skills(min_weight: int = 0):
    """API endpoint for skills."""
    resume = load_resume_data()
    if not resume:
        return JSONResponse({"error": "Resume not found"}, status_code=404)
    
    skills = resume.get('skills', {})
    filtered = {k: v for k, v in skills.items() if v >= min_weight}
    return JSONResponse({"skills": filtered, "count": len(filtered)})

@app.get("/api/get_shortlist")
async def api_get_shortlist():
    """API endpoint for job shortlist."""
    try:
        from match_rank import match_and_rank
        result = match_and_rank(top_n=5)
        if isinstance(result, tuple):
            success, shortlist_df, ranked_df = result
            if success and shortlist_df is not None:
                return JSONResponse({
                    "shortlist": shortlist_df.to_dict(orient="records"),
                    "count": len(shortlist_df)
                })
        return JSONResponse({"error": "No shortlist available"}, status_code=404)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/check_job_match")
async def api_check_job_match(request: Request):
    """API endpoint for job matching."""
    try:
        data = await request.json()
        from match_rank import load_rulebook, filter_jobs, rank_jobs
        import pandas as pd
        
        resume = load_resume_data()
        rulebook = load_rulebook()
        
        job_df = pd.DataFrame([{
            "title": data.get("job_title", ""),
            "company": data.get("company", ""),
            "description": data.get("job_description", ""),
            "url": ""
        }])
        
        filtered_df, discarded_df = filter_jobs(job_df, rulebook)
        if len(filtered_df) == 0:
            return JSONResponse({
                "match": False,
                "reason": "Job filtered out by rulebook"
            })
        
        ranked_df = rank_jobs(filtered_df, resume, rulebook)
        if len(ranked_df) > 0:
            job_result = ranked_df.iloc[0].to_dict()
            return JSONResponse({
                "match": True,
                "match_score": job_result.get("match_score", 0),
                "matched_skills": job_result.get("matched_skills", ""),
                "matched_projects": job_result.get("matched_projects", "")
            })
        
        return JSONResponse({"error": "Failed to rank job"}, status_code=500)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

