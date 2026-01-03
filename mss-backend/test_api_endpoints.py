"""
Test API endpoints for the RAG pipeline
"""

import requests
import json
import time

def test_api_endpoints():
    """Test the API endpoints."""
    base_url = "http://localhost:8001/api/v1"

    print("🚀 Testing API Endpoints...")

    # Wait for server to be ready
    time.sleep(2)

    # Test 1: Health check
    print("\n🏥 Testing health check...")
    try:
        response = requests.get(f"{base_url}/health/status")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

    # Test 2: Root endpoint
    print("\n🏠 Testing root endpoint...")
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Root endpoint passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")

    # Test 3: Document upload (using the test PDF we created)
    print("\n📄 Testing document upload...")
    try:
        with open("test_financial_report.pdf", "rb") as f:
            files = {"file": ("test_financial_report.pdf", f, "application/pdf")}
            response = requests.post(f"{base_url}/documents/upload", files=files)

        if response.status_code == 200:
            result = response.json()
            print("✅ Document upload passed")
            print(f"   Document ID: {result.get('document_id')}")
            print(f"   Processing Method: {result.get('processing_method')}")
            print(f"   Status: {result.get('status')}")

            # Store document ID for later tests
            document_id = result.get('document_id')

            # Test 4: Get document analysis
            print(f"\n📊 Testing get document analysis for {document_id}...")
            try:
                response = requests.get(f"{base_url}/documents/{document_id}")
                if response.status_code == 200:
                    analysis = response.json()
                    print("✅ Get document analysis passed")
                    print(f"   Metrics extracted: {len(analysis.get('metrics', {}))}")
                    print(f"   Risk factors: {len(analysis.get('risk_factors', []))}")
                    print(f"   Recommendations: {len(analysis.get('recommendations', []))}")
                else:
                    print(f"❌ Get document analysis failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Get document analysis error: {e}")

            # Test 5: Get document metrics
            print(f"\n💰 Testing get document metrics for {document_id}...")
            try:
                response = requests.get(f"{base_url}/documents/{document_id}/metrics")
                if response.status_code == 200:
                    metrics = response.json()
                    print("✅ Get document metrics passed")
                    print(f"   Metrics count: {len(metrics.get('metrics', {}))}")
                else:
                    print(f"❌ Get document metrics failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Get document metrics error: {e}")

            # Test 6: Semantic search
            print("\n🔍 Testing semantic search...")
            try:
                data = {"query": "financial performance", "top_k": 2}
                response = requests.post(f"{base_url}/documents/search", json=data)
                if response.status_code == 200:
                    results = response.json()
                    print("✅ Semantic search passed")
                    print(f"   Found {len(results)} results")
                    for i, result in enumerate(results, 1):
                        print(f"   Result {i}: Score {result.get('similarity_score', 0):.3f}")
                else:
                    print(f"❌ Semantic search failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Semantic search error: {e}")

        else:
            print(f"❌ Document upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Document upload error: {e}")

    print(f"\n🎉 API Endpoint Testing Completed!")

if __name__ == "__main__":
    test_api_endpoints()
