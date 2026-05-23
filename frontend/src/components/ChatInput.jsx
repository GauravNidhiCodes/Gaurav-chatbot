import React, { useState, useRef } from 'react'

function ChatInput() {
  const [message, setMessage] = useState('')
  const [attachedFile, setAttachedFile] = useState(null)
  const fileInputRef = useRef(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!message.trim() && !attachedFile) return
    // Handle message send here
    console.log("Sending:", { message, file: attachedFile })
    setMessage('')
    setAttachedFile(null)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleFileClick = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setAttachedFile(file)
    }
    // Reset the input value so the same file can be uploaded again if needed
    e.target.value = null
  }

  return (
    <div className="chat-input-container">
      <form onSubmit={handleSubmit} className="chat-input-wrapper" style={{ flexWrap: 'wrap', flexDirection: 'column' }}>
        {attachedFile && (
          <div style={{ width: '100%', padding: '0.5rem 1rem', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: 'var(--bg-panel)' }}>
            <span style={{ fontSize: '0.875rem', color: 'var(--accent-amber)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
              </svg>
              {attachedFile.name}
            </span>
            <button 
              type="button" 
              onClick={() => setAttachedFile(null)}
              style={{ border: 'none', background: 'transparent', color: 'var(--text-muted)', fontSize: '1rem', padding: '0 0.5rem', cursor: 'pointer' }}
              title="Remove file"
            >
              ✕
            </button>
          </div>
        )}
        <div style={{ display: 'flex', width: '100%' }}>
          <button 
            type="button" 
            onClick={handleFileClick}
            title="Upload File"
            style={{
              padding: '0 1rem',
              background: 'transparent',
              border: 'none',
              borderRight: '1px solid var(--border-color)',
              color: attachedFile ? 'var(--accent-amber)' : 'var(--text-muted)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'color 0.2s ease'
            }}
            onMouseEnter={(e) => e.currentTarget.style.color = 'var(--accent-amber)'}
            onMouseLeave={(e) => e.currentTarget.style.color = attachedFile ? 'var(--accent-amber)' : 'var(--text-muted)'}
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
            </svg>
          </button>
          <input 
            type="file" 
            ref={fileInputRef} 
            style={{ display: 'none' }} 
            onChange={handleFileChange} 
          />
          <textarea
            placeholder="Type a message... (Press Enter to send)"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            rows="1"
          />
          <button type="submit" className="send-btn">
            Send
          </button>
        </div>
      </form>
    </div>
  )
}

export default ChatInput
