from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
from typing import List, Dict

app = FastAPI(title="SparkGPT SEO Engine")

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    return "ok"


# ----------------------------------------
#  🔍 Keyword Analysis (Mock Version)
# ----------------------------------------
@app.get("/analyze-keywords")
def analyze_keywords(keyword: str = Query(..., description="Primary keyword to analyze")) -> Dict:
    # In future: connect to Google APIs / NLP
    # For now: mock realistic structured response
    variations = [
        f"{keyword} strategy",
        f"{keyword} tools",
        f"best {keyword} tips",
        f"{keyword} for beginners",
        f"advanced {keyword} techniques"
    ]

    clusters = {
        "Informational": [f"what is {keyword}", f"how to use {keyword}"],
        "Transactional": [f"buy {keyword}", f"{keyword} pricing"],
        "Commercial": [f"best {keyword} services", f"{keyword} vs competitors"]
    }

    intent = "Informational" if "how" in keyword or "what" in keyword else "Mixed"

    return {
        "keyword": keyword,
        "intent": intent,
        "variations": variations,
        "clusters": clusters,
        "notes": "Mock data. Future version will integrate Google NLP + Search Volume APIs."
    }
