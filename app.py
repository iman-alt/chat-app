from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chatspark_secret_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# ── Database setup ─────────────────────────────────────────────
def init_db():
    """Create the messages table if it doesn't exist."""
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT    NOT NULL,
            message   TEXT    NOT NULL,
            timestamp TEXT    NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_message(username, message, timestamp):
    """Save a chat message to SQLite."""
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)',
        (username, message, timestamp)
    )
    conn.commit()
    conn.close()

def load_messages(limit=50):
    """Load the last N messages from SQLite."""
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT username, message, timestamp FROM messages ORDER BY id DESC LIMIT ?',
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    # Reverse so oldest appears first
    return list(reversed(rows))

# ── Routes ─────────────────────────────────────────────────────
@app.route('/')
def index():
    """Serve the chat page with message history."""
    history = load_messages()
    return render_template('index.html', history=history)

# ── Socket Events ───────────────────────────────────────────────
@socketio.on('connect')
def handle_connect():
    """Called when a user opens the page."""
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    """Called when a user closes the tab."""
    print(f'Client disconnected: {request.sid}')

@socketio.on('send_message')
def handle_message(data):
    """
    Called when a user sends a chat message.
    data = { 'username': '...', 'message': '...' }
    We save it, then BROADCAST it to ALL connected clients.
    """
    username  = data.get('username', 'Anonymous').strip() or 'Anonymous'
    message   = data.get('message', '').strip()
    timestamp = datetime.now().strftime('%H:%M')

    if not message:
        return  # Ignore empty messages

    save_message(username, message, timestamp)

    # emit to ALL clients (broadcast=True)
    emit('receive_message', {
        'username':  username,
        'message':   message,
        'timestamp': timestamp
    }, broadcast=True)

@socketio.on('typing')
def handle_typing(data):
    """Broadcast typing indicator to everyone except the sender."""
    emit('user_typing', {'username': data.get('username', 'Someone')}, broadcast=True, include_self=False)

@socketio.on('stop_typing')
def handle_stop_typing():
    emit('user_stopped_typing', {}, broadcast=True, include_self=False)

# ── Run ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    print("ChatSpark running → http://127.0.0.1:5000")
    socketio.run(app, debug=True)