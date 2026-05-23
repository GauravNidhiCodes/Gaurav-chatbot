import React from 'react'

function Sidebar() {
  const dummyConversations = [
    { id: 1, title: 'React Setup Help', active: true },
    { id: 2, title: 'Explain Quantum Computing', active: false },
    { id: 3, title: 'Debug Node.js App', active: false },
    { id: 4, title: 'Vim Configuration', active: false },
    { id: 5, title: 'Write a poem about code', active: false },
  ]

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo-container serif-text">
          Gaurav AI<span className="blinking-dot"></span>
        </div>
      </div>

      <button className="new-chat-btn">
        <span>+</span> New Chat
      </button>

      <div className="conversations-list">
        {dummyConversations.map((chat) => (
          <div 
            key={chat.id} 
            className={`conversation-item ${chat.active ? 'active' : ''}`}
          >
            {chat.title}
          </div>
        ))}
      </div>

      <div className="sidebar-footer">
        Satyam-X v1.0
      </div>
    </div>
  )
}

export default Sidebar
