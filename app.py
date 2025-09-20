# import json
# import random
# import time
# import threading
# from flask import Flask, render_template, request, jsonify
# from flask_socketio import SocketIO, emit

# # --- Backend Configuration and In-memory 'Database' ---
# app = Flask(_name_)
# app.config['SECRET_KEY'] = 'secret_key'
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# # A simple in-memory database to store events
# # In a real app, this would be a persistent database like Firestore or MongoDB
# events = []
# current_event_id = 0
# event_lock = threading.Lock()

# # Define the sensors and apps for our simulation
# SENSORS = ["Camera", "Microphone", "Location", "Contacts", "Photos"]
# APPS = [
#     "Social Media App",
#     "Messaging App",
#     "Weather App",
#     "Banking App",
#     "Gaming App",
#     "Map App",
#     "Flashlight App"
# ]

# # A simple rule-based 'anomaly detection' engine
# def is_suspicious(event):
#     """
#     Flags events as suspicious based on a simple rule set.
#     In a real system, this would be a complex machine learning model.
#     """
#     suspicious_pairs = {
#         "Flashlight App": ["Microphone", "Location", "Contacts", "Photos"],
#         "Weather App": ["Microphone", "Camera", "Contacts", "Photos"],
#         "Gaming App": ["Contacts", "Photos"]
#     }
#     app = event["app"]
#     sensor = event["sensor"]
#     return app in suspicious_pairs and sensor in suspicious_pairs[app]

# def generate_random_event():
#     """Generates a random device access event."""
#     global current_event_id
#     with event_lock:
#         current_event_id += 1
#         event = {
#             "id": current_event_id,
#             "timestamp": int(time.time()),
#             "app": random.choice(APPS),
#             "sensor": random.choice(SENSORS)
#         }
#         event["suspicious"] = is_suspicious(event)
#         events.append(event)
#         return event

# # --- Real-time Event Generation Thread ---
# def event_generator():
#     """Continuously generates events and sends them to clients."""
#     while True:
#         new_event = generate_random_event()
#         # Emit the new event to all connected clients
#         socketio.emit('new_event', new_event)
#         time.sleep(random.uniform(0.5, 2.0))

# # Start the event generation thread in the background
# thread = threading.Thread(target=event_generator, daemon=True)
# thread.start()

# # --- Flask Routes ---
# @app.route('/')
# def index():
#     """Serves the main HTML page."""
#     return render_template('index.html')

# @app.route('/api/events', methods=['GET'])
# def get_events():
#     """Returns the current list of events."""
#     return jsonify(events)

# # --- WebSocket Event Handlers ---
# @socketio.on('connect')
# def handle_connect():
#     """Handles a new client connection."""
#     print(f"Client connected: {request.sid}")
#     # When a new client connects, send them the last 5 events for context
#     with event_lock:
#         initial_events = events[-5:] if len(events) > 5 else events
#     emit('initial_events', initial_events)

# @socketio.on('disconnect')
# def handle_disconnect():
#     """Handles a client disconnection."""
#     print(f"Client disconnected: {request.sid}")

# if _name_ == '_main_':
#     socketio.run(app, debug=False, allow_unsafe_werkzeug=True, port=5000)







import json
import random
import time
import threading
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

# --- Backend Configuration and In-memory 'Database' ---
app = Flask(__name__)   # ✅ Corrected
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# A simple in-memory database to store events
# In a real app, this would be a persistent database like Firestore or MongoDB
events = []
current_event_id = 0
event_lock = threading.Lock()

# Define the sensors and apps for our simulation
SENSORS = ["Camera", "Microphone", "Location", "Contacts", "Photos"]
APPS = [
    "Social Media App",
    "Messaging App",
    "Weather App",
    "Banking App",
    "Gaming App",
    "Map App",
    "Flashlight App"
]

# A simple rule-based 'anomaly detection' engine
def is_suspicious(event):
    """
    Flags events as suspicious based on a simple rule set.
    In a real system, this would be a complex machine learning model.
    """
    suspicious_pairs = {
        "Flashlight App": ["Microphone", "Location", "Contacts", "Photos"],
        "Weather App": ["Microphone", "Camera", "Contacts", "Photos"],
        "Gaming App": ["Contacts", "Photos"]
    }
    app = event["app"]
    sensor = event["sensor"]
    return app in suspicious_pairs and sensor in suspicious_pairs[app]

def generate_random_event():
    """Generates a random device access event."""
    global current_event_id
    with event_lock:
        current_event_id += 1
        event = {
            "id": current_event_id,
            "timestamp": int(time.time()),
            "app": random.choice(APPS),
            "sensor": random.choice(SENSORS)
        }
        event["suspicious"] = is_suspicious(event)
        events.append(event)
        return event

# --- Real-time Event Generation Thread ---
def event_generator():
    """Continuously generates events and sends them to clients."""
    while True:
        new_event = generate_random_event()
        # Emit the new event to all connected clients
        socketio.emit('new_event', new_event)
        time.sleep(random.uniform(0.5, 2.0))

# Start the event generation thread in the background
thread = threading.Thread(target=event_generator, daemon=True)
thread.start()

# --- Flask Routes ---
@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/events', methods=['GET'])
def get_events():
    """Returns the current list of events."""
    return jsonify(events)

# --- WebSocket Event Handlers ---
@socketio.on('connect')
def handle_connect():
    """Handles a new client connection."""
    print(f"Client connected: {request.sid}")
    # When a new client connects, send them the last 5 events for context
    with event_lock:
        initial_events = events[-5:] if len(events) > 5 else events
    emit('initial_events', initial_events)

@socketio.on('disconnect')
def handle_disconnect():
    """Handles a client disconnection."""
    print(f"Client disconnected: {request.sid}")

if __name__ == '__main__':   # ✅ Corrected
    socketio.run(app, debug=False, allow_unsafe_werkzeug=True, port=4000)
