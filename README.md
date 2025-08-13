# Website Summarizer

A complete end-to-end full-stack application that takes a website URL as input and returns a concise summary of the main points from that website. Built with React frontend and FastAPI backend for efficient web content summarization.

## Features

- 🌐 **Smart Content Extraction**: Uses BeautifulSoup and requests for reliable text extraction from web pages
- 📝 **Intelligent Summarization**: Simple but effective text summarization algorithm
- 🎨 **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- 🚀 **Fast Performance**: Optimized for quick processing and minimal load times
- 🛡️ **Error Handling**: Comprehensive error handling with user-friendly messages
- 📱 **Mobile Responsive**: Works seamlessly across all device sizes
- ⚡ **Real-time Processing**: Loading indicators and instant feedback

## Demo

The application provides:
- A clean form with URL input field and "Summarize" button
- Loading indicator during processing
- Nicely styled summary display in a card format
- Graceful error handling for invalid URLs or processing failures

## Tech Stack

### Frontend
- **React 18** - Modern JavaScript framework with hooks
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework (via CDN)
- **Font Awesome** - Icon library for enhanced UI

### Backend
- **FastAPI** - High-performance Python web framework
- **BeautifulSoup4** - HTML parsing and content extraction
- **Requests** - HTTP library for fetching web pages
- **Uvicorn** - ASGI server for production
- **Pydantic** - Data validation using Python type hints

## Prerequisites

Before running this application, make sure you have:

- **Python 3.11+** installed
- **Node.js 20+** and npm installed
- **Internet connection** for fetching website content

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd website-summarizer
```

### 2. Backend Setup
```bash
cd backend

# Install Python dependencies (using uv or pip)
uv add fastapi uvicorn beautifulsoup4 requests
# OR using pip:
# pip install fastapi uvicorn beautifulsoup4 requests

# Run the backend server (will start on port 8000)
python simple_main.py
```

### 3. Frontend Setup
```bash
cd frontend

# Install Node.js dependencies
npm install

# Run the frontend development server (will start on port 5000)
npm run dev
```

## Usage

1. **Start the Backend**: Navigate to the `backend` folder and run `python simple_main.py`
2. **Start the Frontend**: Navigate to the `frontend` folder and run `npm run dev`
3. **Open the Application**: Visit `http://localhost:5000` in your browser
4. **Summarize Websites**: 
   - Enter any website URL (with or without https://)
   - Click "Summarize Website"
   - View the AI-generated summary

## API Endpoints

### Backend API (Port 8000)

- **GET /** - API status message
- **GET /health** - Health check endpoint
- **POST /summarize** - Main summarization endpoint
  ```json
  {
    "url": "https://example.com"
  }
  ```

## Project Structure

```
website-summarizer/
├── backend/
│   ├── simple_main.py       # Main FastAPI application (simplified version)
│   ├── main.py             # Advanced FastAPI app (with AI models)
│   ├── web_scraper.py      # Web scraping utilities
│   └── summarizer.py       # AI summarization logic
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── SummarizerForm.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Features in Detail

### Content Extraction
- Handles various website formats and structures
- Removes navigation, scripts, and styling elements
- Extracts main readable content
- Supports both HTTP and HTTPS URLs

### Summarization
- Simple extractive summarization using sentence selection
- Limits content length for optimal processing
- Provides meaningful summaries even for short content
- Error handling for edge cases

### User Interface
- Responsive design that works on all devices
- Loading states with spinner animations
- Error messages with helpful suggestions
- Clean, modern styling with Tailwind CSS
- Accessibility features and keyboard navigation

## Troubleshooting

### Common Issues

1. **Backend not starting**: Ensure all Python dependencies are installed
2. **Frontend not loading**: Make sure Node.js and npm are properly installed
3. **CORS errors**: The backend is configured to allow all origins for development
4. **Website not accessible**: Some websites may block automated requests

### Development Notes

- Backend runs on port 8000 by default
- Frontend runs on port 5000 by default  
- CORS is enabled for cross-origin requests
- The application uses `0.0.0.0` for accessible port bindings

## Future Enhancements

- Integration with advanced AI models (BART, T5) for better summarization
- Support for different summary lengths
- Batch processing for multiple URLs
- User authentication and history
- Export functionality for summaries

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
