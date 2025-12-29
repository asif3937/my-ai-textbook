// src/components/AIChat.js
import React, { useState, useRef, useEffect } from 'react';
import './AIChat.css';

const AIChat = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Default book ID for the textbook
  const DEFAULT_BOOK_ID = "bd8add9a-3444-4a7d-978b-ca0952c59bca";

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // Call the backend API
      const response = await fetch('http://127.0.0.1:8000/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: `session-${Date.now()}`,
          query: inputValue,
          mode: 'full_book',
          book_id: DEFAULT_BOOK_ID  // Use the default book ID
        })
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Add assistant response to chat
      const assistantMessage = {
        id: Date.now() + 1,
        text: data.answer,
        sender: 'assistant',
        timestamp: data.timestamp,
        citations: data.citations || []
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError(`Error: ${err.message || 'Failed to send message'}`);
      
      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        text: `Sorry, I encountered an error: ${err.message || 'Failed to get response'}`,
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatCitations = (citations) => {
    if (!citations || citations.length === 0) return null;
    
    return (
      <div className="mt-2 text-xs text-gray-500">
        <p className="font-semibold">Sources:</p>
        <ul className="list-disc pl-5 space-y-1">
          {citations.map((citation, index) => (
            <li key={index}>
              {citation.text.substring(0, 100)}
              {citation.text.length > 100 && '...'}
            </li>
          ))}
        </ul>
      </div>
    );
  };

  return (
    <div className="ai-chat-container">
      <div className="ai-chat-header">
        <h2>AI Textbook Assistant</h2>
        <p>Ask questions about your textbook content</p>
      </div>
      
      <div className="ai-chat-messages">
        {messages.length === 0 ? (
          <div className="ai-chat-welcome">
            <div className="ai-chat-icon">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <p>Ask me anything about your textbook!</p>
            <p className="ai-chat-subtitle">I can answer questions about Physical AI, Humanoid Robotics, ROS2, and more.</p>
          </div>
        ) : (
          <div className="ai-chat-messages-list">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`ai-chat-message ${message.sender === 'user' ? 'ai-chat-user-message' : 'ai-chat-assistant-message'}`}
              >
                <div className={`ai-chat-bubble ${message.sender === 'user' ? 'ai-chat-user-bubble' : message.isError ? 'ai-chat-error-bubble' : 'ai-chat-assistant-bubble'}`}>
                  <div className="ai-chat-message-text">{message.text}</div>
                  {message.sender === 'assistant' && !message.isError && formatCitations(message.citations)}
                  <div className="ai-chat-timestamp">
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="ai-chat-message ai-chat-assistant-message">
                <div className="ai-chat-bubble ai-chat-assistant-bubble ai-chat-loading-bubble">
                  <div className="ai-chat-loading">
                    <span>Thinking</span>
                    <div className="ai-chat-dots">
                      <span className="ai-chat-dot"></span>
                      <span className="ai-chat-dot"></span>
                      <span className="ai-chat-dot"></span>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>
      
      {error && (
        <div className="ai-chat-error">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="ai-chat-input-form">
        <div className="ai-chat-input-container">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask a question about your textbook..."
            className="ai-chat-input"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="ai-chat-send-button"
          >
            Send
          </button>
        </div>
        <p className="ai-chat-powered-by">
          Powered by RAG technology using your textbook content
        </p>
      </form>
    </div>
  );
};

export default AIChat;