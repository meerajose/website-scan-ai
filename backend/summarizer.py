from transformers import pipeline, AutoTokenizer
import torch
import logging
import os

logger = logging.getLogger(__name__)

class TextSummarizer:
    def __init__(self):
        self.summarizer = None
        self.tokenizer = None
        self.max_input_length = 1024
        self.max_output_length = 150
        self.min_output_length = 50
        
    def _initialize_model(self):
        """Initialize the summarization model lazily."""
        if self.summarizer is None:
            try:
                logger.info("Loading BART summarization model...")
                
                # Use CPU if GPU is not available
                device = 0 if torch.cuda.is_available() else -1
                
                # Initialize tokenizer and pipeline
                model_name = "facebook/bart-large-cnn"
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                
                self.summarizer = pipeline(
                    "summarization",
                    model=model_name,
                    tokenizer=self.tokenizer,
                    device=device,
                    framework="pt"
                )
                
                logger.info(f"Model loaded successfully on {'GPU' if device == 0 else 'CPU'}")
                
            except Exception as e:
                logger.error(f"Failed to load summarization model: {str(e)}")
                raise Exception("Failed to initialize AI summarization model. Please try again later.")
    
    def _chunk_text(self, text: str, max_length: int = 900) -> list:
        """Split text into chunks that fit within model's token limit."""
        # Simple sentence-based chunking
        sentences = text.replace('\n', ' ').split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
            if len(current_chunk + sentence) * 0.25 < max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def summarize(self, text: str) -> str:
        """Summarize the given text using BART model."""
        try:
            self._initialize_model()
            
            # Clean input text
            text = text.strip()
            if len(text) < 100:
                return "The provided content is too short to generate a meaningful summary."
            
            # Handle long texts by chunking
            chunks = self._chunk_text(text)
            summaries = []
            
            for i, chunk in enumerate(chunks[:5]):  # Limit to first 5 chunks for performance
                try:
                    logger.info(f"Summarizing chunk {i+1}/{min(len(chunks), 5)}")
                    
                    # Generate summary for this chunk
                    result = self.summarizer(
                        chunk,
                        max_length=self.max_output_length,
                        min_length=self.min_output_length,
                        do_sample=False,
                        truncation=True
                    )
                    
                    if result and len(result) > 0:
                        summary_text = result[0]['summary_text'].strip()
                        if summary_text:
                            summaries.append(summary_text)
                            
                except Exception as e:
                    logger.warning(f"Failed to summarize chunk {i+1}: {str(e)}")
                    continue
            
            if not summaries:
                raise Exception("Failed to generate any summary from the content")
            
            # Combine summaries
            if len(summaries) == 1:
                final_summary = summaries[0]
            else:
                # If multiple summaries, combine and re-summarize
                combined_text = " ".join(summaries)
                if len(combined_text) > 1000:
                    try:
                        result = self.summarizer(
                            combined_text,
                            max_length=self.max_output_length,
                            min_length=self.min_output_length,
                            do_sample=False,
                            truncation=True
                        )
                        final_summary = result[0]['summary_text'].strip()
                    except:
                        # Fallback to truncated combined summary
                        final_summary = combined_text[:500] + "..."
                else:
                    final_summary = combined_text
            
            logger.info("Summary generated successfully")
            return final_summary
            
        except Exception as e:
            logger.error(f"Error in summarization: {str(e)}")
            raise Exception(f"Summarization failed: {str(e)}")

# Global summarizer instance
_summarizer_instance = None

def summarize_text(text: str) -> str:
    """Public function to summarize text."""
    global _summarizer_instance
    
    if _summarizer_instance is None:
        _summarizer_instance = TextSummarizer()
    
    return _summarizer_instance.summarize(text)
