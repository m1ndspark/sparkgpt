from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
from typing import Dict
import os
import openai

app = FastAPI(title="SparkGPT SEO Engine")

# Load the OpenAI API key securely from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    return "ok"


# ----------------------------------------
# 🔍 Keyword Analysis Endpoint
# ----------------------------------------
@app.get("/analyze-keywords")
def analyze_keywords(keyword: str = Query(..., description="Primary keyword to analyze")) -> Dict:
    """
    Provides a structured keyword analysis with sample intent classification
    and cluster groupings. Future versions may integrate Google APIs for
    real-time data and search volume metrics.
    """
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
        "summary": "Keyword segmentation and intent structure generated successfully."
    }


# ----------------------------------------
# ✍️ SEO Content Generator (GPT-powered)
# ----------------------------------------
@app.get("/generate-content")
def generate_content(
    keyword: str = Query(..., description="Primary keyword or topic"),
    content_type: str = Query("article", description="Type: outline, meta, section, or article")
) -> Dict:
    """
    Generates SEO-optimized content using OpenAI GPT based on Google's
    content quality and E-E-A-T guidelines. Supports multiple content types.
    """
    if not openai.api_key:
        return {"error": "Missing OpenAI API key. Add OPENAI_API_KEY in your environment variables."}

    prompt = f"""
    You are an SEO expert content writer.
    Generate a high-quality {content_type} for the topic "{keyword}".
    Apply Google's SEO and E-E-A-T best practices.
    Structure the response clearly, using professional and actionable language.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional SEO strategist and content writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        content = response.choices[0].message["content"].strip()

        return {
            "keyword": keyword,
            "type": content_type,
            "generated_content": content,
            "source": "GPT-4o-mini via OpenAI integration"
        }

    except Exception as e:
        return {"error": str(e)}
