
import ipaddress
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="IP Device Scanner")

app.mount("/static", StaticFiles(directory="static"), name="static")


class ScanRequest(BaseModel):
    ip: str


def ping_device(ip):
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", ip],
            capture_output=True,
            text=True,
            timeout=3
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror, OSError):
        return "Unknown"


def check_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.4)
            return s.connect_ex((ip, port)) == 0
    except OSError:
        return False


def scan_ports(ip):
    common_ports = [21, 22, 23, 53, 80, 443, 445, 3389, 8080]

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(
            lambda port: (port, check_port(ip, port)),
            common_ports
        )

    return [port for port, is_open in results if is_open]


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/api/scan")
def scan_device(request: ScanRequest):
    try:
        address = ipaddress.ip_address(request.ip.strip())

        if not address.is_private or address.is_loopback:
            raise ValueError()

        ip = str(address)

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Enter a valid private network IP address."
        )

    online = ping_device(ip)
    hostname = get_hostname(ip)

    ports = scan_ports(ip) if online else []

    return {
        "ip": ip,
        "status": "Online" if online else "Offline or not responding",
        "hostname": hostname,
        "open_ports": ports
    }
