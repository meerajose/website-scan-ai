# Website Summarizer

## Overview

A full-stack web application that provides AI-powered summaries of website content. The application extracts text from web pages using advanced scraping techniques and generates concise summaries using Facebook's BART neural network model. Built with a React frontend and FastAPI backend, it offers a clean, responsive interface for users to input URLs and receive intelligent summaries of web content.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **React 18 with Vite**: Modern component-based architecture using functional components and hooks for state management
- **Tailwind CSS**: Utility-first CSS framework for rapid UI development and consistent styling
- **Single Page Application (SPA)**: Client-side routing and state management for seamless user experience
- **Responsive Design**: Mobile-first approach ensuring compatibility across all device sizes

### Backend Architecture
- **FastAPI Framework**: High-performance async Python web framework chosen for its automatic API documentation and type validation
- **Modular Design**: Separated concerns with distinct modules for web scraping (`web_scraper.py`) and text summarization (`summarizer.py`)
- **RESTful API**: Simple endpoint structure with `/summarize` for main functionality and `/health` for monitoring
- **Pydantic Models**: Type-safe request/response validation and serialization

### Text Processing Pipeline
- **Trafilatura**: Advanced web content extraction library chosen over basic scrapers for better text quality and handling of various website structures
- **Content Cleaning**: Multi-step text processing including validation, length limits, and format normalization
- **Chunking Strategy**: Sentence-based text splitting to handle content exceeding model token limits

### AI Summarization
- **Facebook BART Model**: Pre-trained transformer model (`facebook/bart-large-cnn`) optimized for news summarization tasks
- **Lazy Loading**: Model initialization only occurs on first request to reduce startup time
- **Hardware Optimization**: Automatic GPU/CPU detection for optimal performance
- **Configurable Parameters**: Adjustable summary length (50-150 tokens) and input processing limits

### Error Handling Strategy
- **Comprehensive Exception Management**: Multiple layers of error handling from URL validation to model failures
- **User-Friendly Messages**: Technical errors are translated into actionable user feedback
- **Graceful Degradation**: System continues operating even if individual requests fail

## External Dependencies

### Core ML Libraries
- **Transformers (Hugging Face)**: Primary library for loading and running the BART summarization model
- **PyTorch**: Deep learning framework required by the transformer models
- **Trafilatura**: Specialized web content extraction with built-in content quality filtering

### Web Framework Dependencies
- **FastAPI**: Main web framework with automatic OpenAPI documentation
- **Uvicorn**: ASGI server for serving the FastAPI application
- **Pydantic**: Data validation and serialization using Python type hints

### Frontend Build Tools
- **Vite**: Modern build tool replacing traditional bundlers for faster development
- **React**: Component library for building the user interface
- **Tailwind CSS**: Loaded via CDN for styling utilities
- **Font Awesome**: Icon library loaded via CDN

### Infrastructure Services
- **CORS Middleware**: Configured for cross-origin requests between frontend and backend
- **HTTP Client Libraries**: Requests and urllib for web scraping operations
- **Logging Framework**: Python's built-in logging for debugging and monitoring

### Model Dependencies
- **Pre-trained BART Model**: Downloaded from Hugging Face model hub on first initialization
- **Tokenizer**: Associated tokenizer for text preprocessing and postprocessing
- **CUDA Support**: Optional GPU acceleration if available in the deployment environment