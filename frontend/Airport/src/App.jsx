import { useEffect, useMemo, useRef, useState } from 'react'
import './App.css'

const createTimestamp = (date = new Date()) =>
  date.toLocaleTimeString([], {
    hour: 'numeric',
    minute: '2-digit',
  })

const initialMessages = [
  {
    id: 1,
    sender: 'ai',
    text: 'Welcome aboard SkyBooking. I can help with flights, baggage questions, upgrades, and booking changes.',
    timestamp: '10:32 AM',
  }
]

function MessageBubble({ message }) {
  const isUser = message.sender === 'user'

  return (
    <article
      className={`message-row ${isUser ? 'message-row-user' : 'message-row-ai'}`}
    >
      {!isUser && (
        <div className="message-avatar message-avatar-ai" aria-hidden="true">
          AA
        </div>
      )}

      <div className="message-stack">
        <div className={`message-bubble ${isUser ? 'message-bubble-user' : 'message-bubble-ai'}`}>
          <p>{message.text}</p>
        </div>
        <time className={`message-time ${isUser ? 'message-time-user' : ''}`}>
          {message.timestamp}
        </time>
      </div>

      {isUser && (
        <div className="message-avatar message-avatar-user" aria-hidden="true">
          YU
        </div>
      )}
    </article>
  )
}

function App() {
  const [messages, setMessages] = useState(initialMessages)
  const [draft, setDraft] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  
  const messageEndRef = useRef(null)
  // ДОДАНО: Створюємо реф для збереження нашого WebSocket з'єднання
  const wsRef = useRef(null)

  const statusLabel = useMemo(
    () => (isTyping ? 'Assistant is typing' : 'Assistant is online'),
    [isTyping],
  )

  // ДОДАНО: Підключення до WebSockets при завантаженні компонента
  useEffect(() => {
    // Вказуємо адресу нашого Django Daphne сервера
    const ws = new WebSocket('ws://127.0.0.1:8000/ws/chat/')
    wsRef.current = ws

    ws.onopen = () => {
      console.log('✅ З\'єднано з Django WebSocket!')
    }

    ws.onmessage = (event) => {
      // Цей код спрацьовує, коли бекенд щось нам надсилає
      const data = JSON.parse(event.data)
      
      const aiMessage = {
        id: Date.now(),
        sender: 'ai',
        text: data.message, // Беремо текст, який надіслав бекенд
        timestamp: createTimestamp(),
      }

      setMessages((currentMessages) => [...currentMessages, aiMessage])
      setIsTyping(false) // Вимикаємо анімацію друку
    }

    ws.onclose = () => {
      console.log('❌ WebSocket відключено')
    }

    // Прибирання при закритті вкладки/компонента
    return () => {
      ws.close()
    }
  }, [])

  // Автоскрол донизу
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages, isTyping])

  const handleSend = () => {
    const trimmedMessage = draft.trim()

    if (!trimmedMessage) return

    // 1. Додаємо повідомлення юзера на екран
    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: trimmedMessage,
      timestamp: createTimestamp(),
    }

    setMessages((currentMessages) => [...currentMessages, userMessage])
    setDraft('')
    setIsTyping(true) // Вмикаємо анімацію "друкує..."

    // 2. ВІДПРАВЛЯЄМО на бекенд замість setTimeout
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      // Відправляємо JSON рівно в тому форматі, який чекає наш consumers.py
      wsRef.current.send(JSON.stringify({
        'message': trimmedMessage
      }))
    } else {
      console.error('WebSocket не підключений!')
      setIsTyping(false)
    }
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSend()
    }
  }

  const handleNewChat = () => {
    setMessages([
      {
        id: Date.now(),
        sender: 'ai',
        text: 'New conversation started. Tell me where you want to fly next, and I will help build the trip.',
        timestamp: createTimestamp(),
      },
    ])
    setDraft('')
    setIsTyping(false)
  }

  return (
    <main className="chat-app">
      <section className="chat-shell" aria-label="SkyBooking AI Assistant">
        <header className="chat-header">
          <div>
            <p className="chat-eyebrow">Aiport Apex</p>
            <h1>SkyBooking AI Assistant</h1>
            <div className="chat-status" aria-live="polite">
              <span className="status-dot" />
              <span>{statusLabel}</span>
            </div>
          </div>

          <button type="button" className="new-chat-button" onClick={handleNewChat}>
            <span className="new-chat-icon" aria-hidden="true">
              +
            </span>
            <span>New Chat</span>
          </button>
        </header>

        <section className="message-panel">
          <div className="message-list">
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}

            {isTyping && (
              <article className="message-row message-row-ai">
                <div className="message-avatar message-avatar-ai" aria-hidden="true">
                  AA
                </div>
                <div className="message-stack">
                  <div className="message-bubble message-bubble-ai typing-bubble">
                    <span>Typing</span>
                    <span className="typing-dots" aria-hidden="true">
                      <span />
                      <span />
                      <span />
                    </span>
                  </div>
                </div>
              </article>
            )}

            <div ref={messageEndRef} />
          </div>
        </section>

        <form
          className="chat-input-bar"
          onSubmit={(event) => {
            event.preventDefault()
            handleSend()
          }}
        >
          <label className="sr-only" htmlFor="chat-message">
            Type your message
          </label>
          <textarea
            id="chat-message"
            className="chat-input"
            rows="1"
            placeholder="Ask about flights, seats, upgrades, or your next itinerary..."
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            onKeyDown={handleKeyDown}
          />

          <button type="submit" className="send-button" disabled={!draft.trim()}>
            <span className="send-icon" aria-hidden="true">
              ↗
            </span>
            <span>Send</span>
          </button>
        </form>
      </section>
    </main>
  )
}

export default App