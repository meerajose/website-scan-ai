import React, { useState } from 'react'

const SummarizerForm = () => {
  const [url, setUrl] = useState('')
  const [summary, setSummary] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const API_BASE_URL = 'http://localhost:8000'

  const validateUrl = (urlString) => {
    try {
      // Add protocol if missing
      if (!urlString.startsWith('http://') && !urlString.startsWith('https://')) {
        urlString = 'https://' + urlString
      }
      
      const url = new URL(urlString)
      return url.protocol === 'http:' || url.protocol === 'https:'
    } catch {
      return false
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Reset states
    setError('')
    setSummary('')
    setSuccess(false)
    
    // Validate input
    if (!url.trim()) {
      setError('Please enter a website URL')
      return
    }
    
    if (!validateUrl(url.trim())) {
      setError('Please enter a valid website URL (e.g., example.com or https://example.com)')
      return
    }

    setLoading(true)

    try {
      let processedUrl = url.trim()
      if (!processedUrl.startsWith('http://') && !processedUrl.startsWith('https://')) {
        processedUrl = 'https://' + processedUrl
      }

      const response = await fetch(`${API_BASE_URL}/summarize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: processedUrl }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || `HTTP error! status: ${response.status}`)
      }

      setSummary(data.summary)
      setSuccess(true)
    } catch (err) {
      console.error('Error:', err)
      setError(err.message || 'Failed to summarize the website. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setUrl('')
    setSummary('')
    setError('')
    setSuccess(false)
  }

  return (
    <div className="bg-white rounded-2xl card-shadow p-8 md:p-12">
      {/* Form */}
      <form onSubmit={handleSubmit} className="mb-8">
        <div className="mb-6">
          <label htmlFor="url" className="block text-sm font-semibold text-gray-700 mb-3">
            Website URL
          </label>
          <div className="relative">
            <input
              type="text"
              id="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter website URL (e.g., example.com or https://example.com)"
              className="w-full px-4 py-4 text-lg border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200 outline-none"
              disabled={loading}
            />
            <i className="fas fa-link absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
          </div>
        </div>

        <div className="flex gap-4">
          <button
            type="submit"
            disabled={loading || !url.trim()}
            className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-4 px-8 rounded-xl hover:from-blue-700 hover:to-purple-700 focus:ring-4 focus:ring-blue-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 text-lg"
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <i className="fas fa-spinner spinner mr-2"></i>
                Summarizing...
              </span>
            ) : (
              <span className="flex items-center justify-center">
                <i className="fas fa-magic mr-2"></i>
                Summarize Website
              </span>
            )}
          </button>

          {(summary || error) && (
            <button
              type="button"
              onClick={handleReset}
              className="bg-gray-500 text-white font-semibold py-4 px-6 rounded-xl hover:bg-gray-600 focus:ring-4 focus:ring-gray-200 transition-all duration-200"
            >
              <i className="fas fa-redo"></i>
            </button>
          )}
        </div>
      </form>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg fade-in">
          <div className="flex items-start">
            <i className="fas fa-exclamation-circle text-red-500 mt-1 mr-3"></i>
            <div>
              <h3 className="text-red-800 font-semibold">Error</h3>
              <p className="text-red-700 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Success Summary */}
      {success && summary && (
        <div className="fade-in">
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-xl font-bold text-gray-800 flex items-center">
              <i className="fas fa-file-alt text-blue-600 mr-2"></i>
              Summary
            </h3>
            <div className="flex items-center text-sm text-gray-500">
              <i className="fas fa-check-circle text-green-500 mr-1"></i>
              Generated successfully
            </div>
          </div>
          
          <div className="bg-gray-50 border-l-4 border-blue-500 p-6 rounded-lg">
            <div className="mb-3">
              <span className="text-sm font-medium text-gray-600">Source:</span>
              <p className="text-sm text-blue-600 break-all mt-1">{url}</p>
            </div>
            
            <div>
              <span className="text-sm font-medium text-gray-600 block mb-2">AI Summary:</span>
              <div className="prose prose-lg max-w-none">
                <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">
                  {summary}
                </p>
              </div>
            </div>
          </div>

          {/* Summary Stats */}
          <div className="mt-4 flex flex-wrap gap-4 text-sm text-gray-500">
            <span>
              <i className="fas fa-text-width mr-1"></i>
              {summary.length} characters
            </span>
            <span>
              <i className="fas fa-align-left mr-1"></i>
              ~{Math.ceil(summary.split(' ').length / 200)} min read
            </span>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="text-center py-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
            <i className="fas fa-cog fa-2x text-blue-600 spinner"></i>
          </div>
          <h3 className="text-lg font-semibold text-gray-700 mb-2">Processing Your Request</h3>
          <p className="text-gray-500">
            Fetching and analyzing website content. This may take a few moments...
          </p>
        </div>
      )}

      {/* Instructions */}
      {!loading && !summary && !error && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-800 mb-3 flex items-center">
            <i className="fas fa-info-circle mr-2"></i>
            How it works
          </h3>
          <ul className="space-y-2 text-blue-700">
            <li className="flex items-start">
              <i className="fas fa-chevron-right text-blue-500 mt-1 mr-2 text-xs"></i>
              Enter any website URL (with or without https://)
            </li>
            <li className="flex items-start">
              <i className="fas fa-chevron-right text-blue-500 mt-1 mr-2 text-xs"></i>
              Our AI extracts and analyzes the main content
            </li>
            <li className="flex items-start">
              <i className="fas fa-chevron-right text-blue-500 mt-1 mr-2 text-xs"></i>
              Get a concise, intelligent summary in seconds
            </li>
          </ul>
        </div>
      )}
    </div>
  )
}

export default SummarizerForm
