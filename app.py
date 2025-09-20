<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Privacy Control System</title>
  <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
  <style>
    body {
      font-family: 'Poppins', sans-serif;
      background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
      color: #f5f5f5;
      margin: 0;
      padding: 0;
      overflow-x: hidden;
    }

    header {
      background: linear-gradient(90deg, #ff416c, #ff4b2b);
      padding: 25px;
      text-align: center;
      font-size: 32px;
      font-weight: 700;
      letter-spacing: 1.5px;
      color: #fff;
      text-transform: uppercase;
      text-shadow: 0px 3px 6px rgba(0,0,0,0.5);
      animation: slideDown 1s ease-out;
    }

    @keyframes slideDown {
      from { transform: translateY(-100%); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    .container {
      max-width: 900px;
      margin: 30px auto;
      background: rgba(255, 255, 255, 0.07);
      padding: 25px 35px;
      border-radius: 20px;
      box-shadow: 0 8px 25px rgba(0,0,0,0.6);
      animation: fadeIn 1.2s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: scale(0.9); }
      to { opacity: 1; transform: scale(1); }
    }

    h2 {
      text-align: center;
      margin-bottom: 20px;
      font-size: 26px;
      font-weight: 600;
      color: #ffcc70;
      text-shadow: 0px 2px 4px rgba(0,0,0,0.5);
      animation: glow 2s infinite alternate;
    }

    @keyframes glow {
      from { text-shadow: 0 0 10px #ffcc70, 0 0 20px #ff6f61; }
      to { text-shadow: 0 0 20px #ffcc70, 0 0 40px #ff6f61; }
    }

    .event-list {
      list-style: none;
      padding: 0;
      margin: 0;
    }

    .event-card {
      background: rgba(255,255,255,0.15);
      margin: 12px 0;
      padding: 18px;
      border-radius: 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: 0.4s ease;
      transform: translateY(20px);
      opacity: 0;
      animation: slideUp 0.6s ease forwards;
    }

    @keyframes slideUp {
      from { transform: translateY(20px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    .event-card:hover {
      transform: scale(1.05);
      box-shadow: 0 6px 20px rgba(0,0,0,0.6);
    }

    .event-info {
      flex: 1;
    }

    .app {
      font-weight: bold;
      font-size: 20px;
      margin-bottom: 4px;
    }

    .sensor {
      font-size: 15px;
      opacity: 0.95;
    }

    .timestamp {
      font-size: 13px;
      color: #ddd;
      margin-top: 3px;
    }

    .status {
      padding: 8px 14px;
      border-radius: 25px;
      font-size: 14px;
      font-weight: bold;
      text-transform: uppercase;
      box-shadow: 0 3px 10px rgba(0,0,0,0.4);
    }

    .safe {
      background: linear-gradient(45deg, #00c853, #64dd17);
      color: white;
    }

    .suspicious {
      background: linear-gradient(45deg, #ff1744, #d50000);
      color: white;
      animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
      0% { transform: scale(1); box-shadow: 0 0 10px #ff1744; }
      50% { transform: scale(1.05); box-shadow: 0 0 25px #d50000; }
      100% { transform: scale(1); box-shadow: 0 0 10px #ff1744; }
    }
  </style>
</head>
<body>
  <header>🔒 Privacy Control System</header>

  <div class="container">
    <h2>📡 Real-Time Device Access Events</h2>
    <ul class="event-list" id="events"></ul>
  </div>

  <script>
    const socket = io();

    function formatTime(ts) {
      const date = new Date(ts * 1000);
      return date.toLocaleString();
    }

    function addEvent(event) {
      const list = document.getElementById("events");
      const li = document.createElement("li");
      li.className = "event-card";

      li.innerHTML = `
        <div class="event-info">
          <div class="app">📱 ${event.app}</div>
          <div class="sensor">🛠 Sensor: ${event.sensor}</div>
          <div class="timestamp">⏰ ${formatTime(event.timestamp)}</div>
        </div>
        <div class="status ${event.suspicious ? 'suspicious' : 'safe'}">
          ${event.suspicious ? 'Suspicious' : 'Safe'}
        </div>
      `;

      // Add at the top
      list.insertBefore(li, list.firstChild);

      // Limit to last 10
      if (list.childElementCount > 10) {
        list.removeChild(list.lastChild);
      }
    }

    socket.on("initial_events", (data) => {
      data.forEach(addEvent);
    });

    socket.on("new_event", (data) => {
      addEvent(data);
    });
  </script>
</body>
</html>
