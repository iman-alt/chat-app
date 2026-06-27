# ChatSpark ⚡

> Real-time multi-user chat app built with Flask, WebSockets, and SQLite.

## Tech Stack
- **Backend:** Python, Flask, Flask-SocketIO, Eventlet
- **Frontend:** Vanilla JS, Socket.IO client
- **Database:** SQLite (messages persist across sessions)
- **Styling:** Custom CSS — teal, coral, amber, purple, pink, green palette

## Features
- Real-time messaging via WebSockets
- Username entry on join
- Typing indicator
- Message history (last 50 messages loaded on page open)
- Messages persisted to SQLite
- Works across multiple browser tabs / devices on the same network

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/iman-alt/chat-app.git
cd chat-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open in browser
# http://127.0.0.1:5000
# Open in TWO tabs and chat with yourself!
```

## Project Structure

chat-app/

├── app.py          # Flask app + SocketIO events

├── chat.db         # SQLite database (auto-created)

├── requirements.txt

├── README.md

└── templates/

└── index.html  # Full chat UI

## How WebSockets Work (Simple)
Normal HTTP = letters (you ask, server replies, connection closes).  
WebSocket = phone call (connection stays open, both sides talk anytime).  
Flask-SocketIO handles this — when you `emit()` a message, it broadcasts to all connected clients instantly.
