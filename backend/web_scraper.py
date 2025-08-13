import trafilatura
import requests
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

def get_website_text_content(url: str) -> str:
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    The results is not directly readable, better to be summarized by LLM before consume
    by the user.

    Some common website to crawl information from:
    MLB scores: https://www.mlb.com/scores/YYYY-MM-DD
    """
    try:
        # Validate URL format
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL format")
        
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        logger.info(f"Fetching content from URL: {url}")
        
        # Send a request to the website with timeout and headers
        downloaded = trafilatura.fetch_url(
            url, 
            config=trafilatura.settings.use_config()
        )
        
        if not downloaded:
            raise Exception("Failed to download content from the URL")
        
        # Extract text content
        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=True,
            include_formatting=False
        )
        
        if not text:
            raise Exception("No readable content found on the webpage")
        
        # Clean and validate extracted text
        text = text.strip()
        if len(text) < 50:  # Minimum content length
            raise Exception("Extracted content is too short to summarize")
        
        logger.info(f"Successfully extracted {len(text)} characters from {url}")
        return text
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while fetching {url}: {str(e)}")
        raise Exception(f"Network error: Unable to reach the website. Please check your internet connection and try again.")
    
    except Exception as e:
        logger.error(f"Error extracting content from {url}: {str(e)}")
        raise Exception(f"Content extraction failed: {str(e)}")
