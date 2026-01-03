"""Quick test of API endpoints"""
import time
import subprocess
import requests
import json
import os
import sys

# Fix encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Set environment variables
os.chdir('C:\\Users\\Joseph\\Desktop\\projects\\Wizcoders-Mclaren-Orix-Hackathon\\mss-backend')
env = os.environ.copy()

# Start the server
print("Starting server...")
server_proc = subprocess.Popen(
    ["python", "-m", "uvicorn", "src.main:app", "--port", "8001"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env
)

# Wait for server to start - longer wait
print("Waiting for server to start...")
time.sleep(8)

try:
    # Test 1: Health check
    print("\nTesting health check...")
    try:
        response = requests.get("http://localhost:8001/api/v1/health/status", timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Connection error: {e}")

    # Test 2: Root endpoint
    print("\nTesting root endpoint...")
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Connection error: {e}")

    # Test 3: Document upload
    print("\nTesting document upload...")
    try:
        with open("test_financial_report.pdf", "rb") as f:
            files = {"file": ("test_financial_report.pdf", f, "application/pdf")}
            response = requests.post("http://localhost:8001/api/v1/documents/upload", files=files, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Document ID: {result.get('document_id')}")
            print(f"Status: {result.get('status')}")
            print(f"Processing Method: {result.get('processing_method')}")
            print(f"Processing Time: {result.get('processing_time_ms')}ms")
            print(f"Metrics extracted: {len(result.get('extracted_metrics', {}))} fields")
            print(f"Risk Factors: {len(result.get('risk_factors', []))} found")
            print(f"Recommendations: {len(result.get('recommendations', []))} provided")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

finally:
    print("\nShutting down server...")
    server_proc.terminate()
    try:
        server_proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server_proc.kill()
        server_proc.wait()


