from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import uvicorn
import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Website Summarizer API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: HttpUrl

class SummaryResponse(BaseModel):
    summary: str
    url: str
    success: bool

def extract_text_from_url(url: str) -> str:
    """Extract text content from a website URL using requests and BeautifulSoup."""
    try:
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:5000]  # Limit to first 5000 characters
        
    except Exception as e:
        logger.error(f"Error extracting text from {url}: {str(e)}")
        raise Exception(f"Failed to extract content: {str(e)}")

def simple_summarize(text: str) -> str:
    """Create a simple summary by extracting key sentences."""
    if not text or len(text) < 100:
        return "The content is too short to summarize effectively."
    
    # Split into sentences
    sentences = text.split('. ')
    
    # Take first few sentences and some from middle as a simple summary
    if len(sentences) <= 3:
        return text[:500] + "..."
    
    # Simple extractive summary: first 2 sentences + a middle sentence
    summary_parts = []
    summary_parts.extend(sentences[:2])
    
    if len(sentences) > 5:
        middle_idx = len(sentences) // 2
        summary_parts.append(sentences[middle_idx])
    
    summary = '. '.join(summary_parts)
    
    # Ensure it's not too long
    if len(summary) > 800:
        summary = summary[:800] + "..."
    
    return summary

@app.get("/")
async def root():
    return {"message": "Website Summarizer API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/summarize", response_model=SummaryResponse)
async def summarize_website(request: URLRequest):
    """
    Summarize the content of a website given its URL.
    """
    try:
        url_str = str(request.url)
        logger.info(f"Processing summarization request for URL: {url_str}")
        
        # Extract text content from the website
        try:
            text_content = extract_text_from_url(url_str)
            if not text_content or len(text_content.strip()) < 50:
                raise HTTPException(
                    status_code=400, 
                    detail="Unable to extract meaningful content from the provided URL. The website might be empty, require JavaScript, or be inaccessible."
                )
        except Exception as e:
            logger.error(f"Error extracting content from {url_str}: {str(e)}")
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to fetch or parse the website content. Please check if the URL is valid and accessible."
            )
        
        # Generate summary
        try:
            summary = simple_summarize(text_content)
        except Exception as e:
            logger.error(f"Error summarizing content: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail="Failed to generate summary due to an internal error."
            )
        
        logger.info(f"Successfully summarized content for URL: {url_str}")
        return SummaryResponse(
            summary=summary,
            url=url_str,
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing request: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="An unexpected error occurred while processing your request."
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)