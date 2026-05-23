import React from 'react'
import ChatInput from './ChatInput'

function MainChat() {
  const dummyMessages = [
    {
      id: 1,
      sender: 'user',
      text: 'Hello! I need some help setting up a Vite project with React.'
    },
    {
      id: 2,
      sender: 'bot',
      text: 'Initialization sequence started. I am Satyam-X. I can assist you with Vite and React. To begin, you can run `npm create vite@latest my-app -- --template react` in your terminal. What specific help do you need?'
    },
    {
      id: 3,
      sender: 'user',
      text: 'Thanks! How do I add CSS variables and pure CSS without any UI frameworks?'
    },
    {
      id: 4,
      sender: 'bot',
      text: 'Excellent choice. To implement pure CSS with variables:\n\n1. Define your tokens in `:root` inside `index.css`.\n2. Apply them using `var(--variable-name)`.\n3. Avoid importing libraries like Tailwind or MUI.\n4. Enforce strict brutalist styling by setting `border-radius: 0 !important;` globally.\n\nReady for the next directive.'
    }
  ]

  return (
    <div className="main-chat">
      <div className="chat-header serif-text">
        <span className="amber-text" style={{ marginRight: '8px' }}>/</span> React Setup Help
      </div>

      <div className="chat-feed">
        {dummyMessages.map((msg) => (
          <div key={msg.id} className={`message ${msg.sender}`}>
            <div className="message-sender">
              {msg.sender === 'user' ? 'You' : 'Gaurav AI'}
            </div>
            <div className="message-content">
              {/* Preserving whitespace for simple code/text formatting */}
              <span style={{ whiteSpace: 'pre-wrap' }}>{msg.text}</span>
            </div>
          </div>
        ))}
      </div>

      <ChatInput />
    </div>
  )
}

export default MainChat
