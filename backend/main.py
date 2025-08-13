from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import uvicorn
from web_scraper import get_website_text_content
from summarizer import summarize_text
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
            text_content = get_website_text_content(url_str)
            if not text_content:
                raise HTTPException(
                    status_code=400, 
                    detail="Unable to extract meaningful content from the provided URL. The website might be empty, require JavaScript, or be inaccessible."
                )
        except Exception as e:
            logger.error(f"Error extracting content from {url_str}: {str(e)}")
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to fetch or parse the website content. Please check if the URL is valid and accessible. Error: {str(e)}"
            )
        
        # Summarize the extracted text
        try:
            summary = summarize_text(text_content)
            if not summary:
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to generate summary. The content might be too short or incompatible with the summarization model."
                )
        except Exception as e:
            logger.error(f"Error summarizing content: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to generate summary due to an internal error. Please try again later. Error: {str(e)}"
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
            detail=f"An unexpected error occurred while processing your request. Please try again later."
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
