"""
Test JWT Authentication is Working
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Test all authentication endpoints"""
    print("\n" + "="*70)
    print("🧪 TESTING JWT AUTHENTICATION ENDPOINTS")
    print("="*70)
    
    # Test 1: Health check
    print("\n1️⃣ Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Register a test user
    print("\n2️⃣ Testing user registration...")
    test_user = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "health_goals": ["weight_loss"],
        "dietary_preferences": ["vegetarian"],
        "allergies": ["peanuts"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=test_user)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            token = data.get('access_token')
            print(f"   ✅ Registration successful!")
            print(f"   Token received: {'Yes' if token else 'No'}")
            return token
        else:
            print(f"   Response: {response.json()}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None
    
    # Test 3: Login with test user
    print("\n3️⃣ Testing user login...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"   ✅ Login successful!")
            print(f"   Token: {token[:50]}...")
            return token
        else:
            print(f"   Response: {response.json()}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_protected_endpoints(token):
    """Test protected endpoints with JWT token"""
    if not token:
        print("\n❌ No token available. Skipping protected endpoint tests.")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 4: Get current user info
    print("\n4️⃣ Testing protected endpoint (GET /me)...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✅ Protected endpoint accessible!")
            print(f"   User: {user_data.get('email')}")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Verify token
    print("\n5️⃣ Testing token verification...")
    try:
        response = requests.post(f"{BASE_URL}/api/auth/verify", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Token is valid!")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Logout
    print("\n6️⃣ Testing logout...")
    try:
        response = requests.post(f"{BASE_URL}/api/auth/logout", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Logout successful!")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def check_server_status():
    """Check if server is running"""
    print("\n🔍 Checking server status...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("   ✅ Server is running!")
            print(f"   Response: {response.json().get('status', 'unknown')}")
            return True
        else:
            print(f"   ❌ Server returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Server is not running!")
        print("   Start the server with: python run.py")
        return False

if __name__ == "__main__":
    print("\n" + "="*70)
    print("JWT AUTHENTICATION TESTER")
    print("="*70)
    
    # Check if server is running
    if not check_server_status():
        sys.exit(1)
    
    # Test endpoints
    token = test_endpoints()
    
    # Test protected endpoints if we got a token
    if token:
        test_protected_endpoints(token)
    
    print("\n" + "="*70)
    print("📋 TEST SUMMARY")
    print("="*70)
    print("\n🎯 To test with your frontend:")
    print("   1. Make sure frontend runs on http://localhost:3000")
    print("   2. Configure axios/fetch to use the token")
    print("   3. Add Authorization header: 'Bearer YOUR_TOKEN'")
    print("\n🔄 To test manually:")
    print("   curl -X POST http://localhost:8000/api/auth/register \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"email\":\"test@example.com\",\"password\":\"test123\"}'")
    print("\n" + "="*70)