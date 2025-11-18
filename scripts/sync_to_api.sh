#!/bin/bash
# Sync clean data to shared FastAPI endpoint

set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Default API URL if not set
API_URL="${API_URL:-http://localhost:8000}"

# Check if files exist
if [ ! -f "jobs_clean.csv" ]; then
    echo "Error: jobs_clean.csv not found. Run etl_clean.py first."
    exit 1
fi

if [ ! -f "shortlist.csv" ]; then
    echo "Error: shortlist.csv not found. Run match_rank.py first."
    exit 1
fi

# Check if Python requests available
if ! python3 -c "import requests" 2>/dev/null; then
    echo "Error: requests library not installed. Run: pip install requests"
    exit 1
fi

echo "Syncing to API: $API_URL"

# Post jobs_clean.csv
echo "Posting jobs_clean.csv..."
python3 << EOF
import requests
import pandas as pd
import json
import os

api_url = os.environ.get('API_URL', 'http://localhost:8000')
df = pd.read_csv('jobs_clean.csv')
jobs_data = df.to_dict('records')

try:
    response = requests.post(
        f"{api_url}/resume/jobs",
        json={"jobs": jobs_data},
        timeout=10
    )
    response.raise_for_status()
    print(f"✓ Posted {len(jobs_data)} jobs successfully")
except requests.exceptions.RequestException as e:
    print(f"✗ Error posting jobs: {e}")
    exit(1)
EOF

# Post shortlist.csv
echo "Posting shortlist.csv..."
python3 << EOF
import requests
import pandas as pd
import json
import os

api_url = os.environ.get('API_URL', 'http://localhost:8000')
df = pd.read_csv('shortlist.csv')
shortlist_data = df.to_dict('records')

try:
    response = requests.post(
        f"{api_url}/resume/shortlist",
        json={"shortlist": shortlist_data},
        timeout=10
    )
    response.raise_for_status()
    print(f"✓ Posted {len(shortlist_data)} shortlist items successfully")
except requests.exceptions.RequestException as e:
    print(f"✗ Error posting shortlist: {e}")
    exit(1)
EOF

echo "✓ Sync complete!"

