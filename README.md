# IP Device Scanner

A lightweight web app for scanning devices on your local network. Enter an IP address to check if a device is online, resolve its hostname, and detect common open ports — all from a simple browser UI.

## Features

- Ping check to determine if a device is online
- Hostname resolution via reverse DNS
- Port scan of common ports (21, 22, 23, 53, 80, 443, 445, 3389, 8080)
- Clean dark-themed web interface
- Only accepts private network IPs (security safeguard)

## Requirements

- Python 3.10+
- pip

See [setup.txt](setup.txt) for detailed installation instructions.

## Quick Start

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000** in your browser.

## How It Works

- `POST /api/scan` — accepts `{"ip": "192.168.1.105"}` and returns status, hostname, and open ports
- `GET /` — serves the web interface from `static/index.html`

The scanner validates that the target is a private (non-loopback) IP before running checks.

## Project Structure

```
IPDeviceScanner/
├── main.py              # FastAPI app and scan logic
├── requirements.txt     # Dependencies (fastapi, uvicorn)
├── setup.txt            # Detailed setup instructions
├── static/
│   └── index.html       # Web UI
└── venv/                # Virtual environment (not committed)
```
