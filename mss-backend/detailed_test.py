"""Detailed test of API endpoints"""
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

# Wait for server to start
print("Waiting for server to start...")
for i in range(15):
    time.sleep(1)
    print(f"  {i+1}/15 seconds...")


try:
    # Test document upload with detailed output
    print("\nTesting document upload...")
    try:
        with open("test_financial_report.pdf", "rb") as f:
            files = {"file": ("test_financial_report.pdf", f, "application/pdf")}
            response = requests.post("http://localhost:8001/api/v1/documents/upload", files=files, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"\nDocument ID: {result.get('document_id')}")
            print(f"Status: {result.get('status')}")
            print(f"Processing Method: {result.get('processing_method')}")
            print(f"Processing Time: {result.get('processing_time_ms')}ms")
            
            # Metrics
            metrics = result.get('extracted_metrics', {})
            print(f"\nExtracted Metrics ({len(metrics)} fields):")
            for key, value in metrics.items():
                if value is not None:
                    print(f"  {key}: {value}")
            
            # Risk Factors
            risk_factors = result.get('risk_factors', [])
            print(f"\nRisk Factors ({len(risk_factors)}):")
            for rf in risk_factors:
                if isinstance(rf, dict):
                    print(f"  - {rf.get('factor', 'Unknown')}")
                    print(f"    Severity: {rf.get('severity', 'N/A')}")
                    print(f"    Description: {rf.get('description', 'N/A')}")
                else:
                    print(f"  - {rf}")
            
            # Recommendations
            recommendations = result.get('recommendations', [])
            print(f"\nRecommendations ({len(recommendations)}):")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
            
            # Analysis
            analysis = result.get('analysis', {})
            print(f"\nAnalysis Summary:")
            print(f"  {analysis.get('summary', 'N/A')}")
            print(f"\nAI Insights:")
            print(f"  {analysis.get('ai_insights', 'N/A')}")
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
