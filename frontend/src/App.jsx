import { useState, useRef, useEffect } from 'react'
import './App.css'

function App() {
  const [apiKey, setApiKey] = useState('')
  const [selectedPdf, setSelectedPdf] = useState('')
  const [userMessage, setUserMessage] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [health, setHealth] = useState(null)
  const [pdfs, setPdfs] = useState([])
  const [uploadMessage, setUploadMessage] = useState('')
  const abortController = useRef(null)
  const fileInputRef = useRef(null)

  // Health check and load PDFs on mount
  useEffect(() => {
    fetch('/api/health')
      .then(res => res.json())
      .then(data => setHealth(data.status === 'ok'))
      .catch(() => setHealth(false))
    
    loadPdfs()
  }, [])

  const loadPdfs = async () => {
    try {
      const res = await fetch('/api/pdfs')
      const data = await res.json()
      console.log('PDFs loaded:', data)  //This is for debugging

      setPdfs(data.pdfs)
      if (data.pdfs.length > 0 && !selectedPdf) {
        setSelectedPdf(data.pdfs[0].id)
      }
    } catch (error) {
      console.error('Error loading PDFs:', error)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setUploadMessage('❌ Only PDF files are allowed')
      return
    }

    if (!apiKey) {
      setUploadMessage('❌ Please enter your OpenAI API key first')
      return
    }

    setUploading(true)
    setUploadMessage('📤 Uploading and indexing PDF...')

    const formData = new FormData()
    formData.append('file', file)
    formData.append('api_key', apiKey)

    try {
      const res = await fetch('/api/upload-pdf', {
        method: 'POST',
        body: formData
      })

      if (!res.ok) {
        const error = await res.json()
        throw new Error(error.detail || 'Upload failed')
      }

      const data = await res.json()
      setUploadMessage(`✅ ${data.message} (${data.chunks_count} chunks indexed)`)
      
      // Reload PDFs list
      await loadPdfs()
      
      // Select the newly uploaded PDF
      setSelectedPdf(data.pdf_id)
      
      // Clear file input
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    } catch (error) {
      setUploadMessage(`❌ Error: ${error.message}`)
    } finally {
      setUploading(false)
    }
  }

  const handleDeletePdf = async (pdfId) => {
    try {
      const res = await fetch(`/api/pdfs/${pdfId}`, {
        method: 'DELETE'
      })

      if (!res.ok) {
        throw new Error('Failed to delete PDF')
      }

      // Reload PDFs list
      await loadPdfs()
      
      // Clear selection if deleted PDF was selected
      if (selectedPdf === pdfId) {
        setSelectedPdf('')
      }
    } catch (error) {
      console.error('Error deleting PDF:', error)
    }
  }

  const handleSend = async (e) => {
    e.preventDefault()
    
    if (!selectedPdf) {
      setResponse('❌ Please select a PDF to chat with')
      return
    }

    if (!userMessage.trim()) {
      setResponse('❌ Please enter a message')
      return
    }

    setResponse('')
    setLoading(true)
    abortController.current = new AbortController()
    
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_message: userMessage,
          pdf_id: selectedPdf,
          api_key: apiKey
        }),
        signal: abortController.current.signal
      })
      
      if (!res.ok) {
        const error = await res.json()
        throw new Error(error.detail || 'Chat request failed')
      }
      
      if (!res.body) throw new Error('No response body')
      
      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let done = false
      
      while (!done) {
        const { value, done: doneReading } = await reader.read()
        done = doneReading
        if (value) setResponse(prev => prev + decoder.decode(value))
      }
    } catch (err) {
      setResponse('Error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleAbort = () => {
    if (abortController.current) abortController.current.abort()
    setLoading(false)
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <h1>📚 PDF RAG Chat</h1>
            <p>Upload PDFs and chat with them using AI</p>
          </div>
          <div className="health-status">
            <span className={`status-indicator ${health ? 'online' : 'offline'}`}>
              {health === null ? '⏳' : health ? '🟢' : '🔴'}
            </span>
            {health === null ? 'Checking...' : health ? 'API Online' : 'API Offline'}
          </div>
        </div>
      </header>
      
      <main className="main-content">
        <div className="container">
          {/* API Key Section */}
          <div className="form-section">
            <h2>🔑 OpenAI API Key</h2>
            <label>
              <input 
                value={apiKey} 
                onChange={e => setApiKey(e.target.value)} 
                type="password" 
                placeholder="sk-..."
                required 
                className="api-key-input"
              />
            </label>
          </div>

          {/* PDF Upload Section */}
          <div className="form-section">
            <h2>📄 Upload PDF</h2>
            <div className="upload-section">
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                onChange={handleFileUpload}
                disabled={uploading}
                className="file-input"
              />
              {uploadMessage && (
                <div className={`upload-message ${uploadMessage.includes('✅') ? 'success' : 'error'}`}>
                  {uploadMessage}
                </div>
              )}
            </div>
          </div>

          {/* PDF Selection Section */}
          {pdfs.length > 0 && (
            <div className="form-section">
              <h2>📚 Available PDFs</h2>
              <div className="pdf-list">
                {pdfs.map(pdf => (
                  <div key={pdf.id} className={`pdf-item ${selectedPdf === pdf.id ? 'selected' : ''}`}>
                    <div className="pdf-info">
                      <span className="pdf-name">{pdf.filename}</span>
                      <span className="pdf-chunks">{pdf.chunks_count} chunks</span>
                    </div>
                    <div className="pdf-actions">
                      <button
                        onClick={() => setSelectedPdf(pdf.id)}
                        className="select-button"
                        disabled={selectedPdf === pdf.id}
                      >
                        {selectedPdf === pdf.id ? '✓ Selected' : 'Select'}
                      </button>
                      <button
                        onClick={() => handleDeletePdf(pdf.id)}
                        className="delete-button"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Chat Section */}
          <div className="form-section">
            <h2>💬 Chat with PDF</h2>
            <form className="chat-form" onSubmit={handleSend}>
              <label>
                <textarea 
                  value={userMessage} 
                  onChange={e => setUserMessage(e.target.value)} 
                  placeholder="Ask a question about your PDF..."
                  required 
                  disabled={!selectedPdf}
                  className="chat-input"
                />
              </label>
              
              <div className="form-actions">
                <button 
                  type="submit" 
                  disabled={loading || !selectedPdf} 
                  className="send-button"
                >
                  {loading ? '🔄 Sending...' : '📤 Send Message'}
                </button>
                <button 
                  type="button" 
                  onClick={handleAbort}
                  disabled={!loading}
                  className={loading ? 'abort-button' : 'abort-button-disabled'}
                >
                  ⏹️ Abort
                </button>
              </div>
            </form>
          </div>
          
          {/* Response Section */}
          <div className="response-section">
            <h2>🤖 AI Response</h2>
            <div className="response-box">
              {response ? (
                <pre>{response}</pre>
              ) : (
                <div className="empty-response">
                  <p>💬 Your response will appear here...</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
