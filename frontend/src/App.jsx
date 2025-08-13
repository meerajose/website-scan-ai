import React from 'react'
import SummarizerForm from './components/SummarizerForm'

function App() {
  return (
    <div className="min-h-screen gradient-bg">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            <i className="fas fa-globe mr-3"></i>
            Website Summarizer
          </h1>
          <p className="text-xl text-white opacity-90 max-w-2xl mx-auto">
            Get concise, AI-powered summaries of any website's content instantly. 
            Simply paste a URL and let our advanced summarization technology do the work.
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          <SummarizerForm />
        </div>

        {/* Footer */}
        <div className="text-center mt-16 text-white opacity-70">
          <p className="text-sm">
            Powered by AI • Built with React & FastAPI • 
            <i className="fas fa-heart text-red-400 mx-1"></i>
            Made for efficient content consumption
          </p>
        </div>
      </div>
    </div>
  )
}

export default App
