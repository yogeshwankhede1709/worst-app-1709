#!/usr/bin/env python3
"""
Backend API Testing Script
Tests all CRUD endpoints for blogs, tools, path, and community features
"""

import requests
import json
import sys
from datetime import datetime
import os
from pathlib import Path

# Load backend URL from frontend .env
def load_backend_url():
    frontend_env = Path("/app/frontend/.env")
    if frontend_env.exists():
        with open(frontend_env) as f:
            for line in f:
                if line.startswith("REACT_APP_BACKEND_URL="):
                    return line.split("=", 1)[1].strip()
    return "http://localhost:8001"

BASE_URL = load_backend_url()
API_URL = f"{BASE_URL}/api"

print(f"Testing backend at: {API_URL}")

# Test results tracking
test_results = []
created_ids = {
    'blog': None,
    'tool': None, 
    'path': None,
    'channel': None,
    'message': None
}

def log_test(test_name, success, details=""):
    """Log test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {test_name}")
    if details:
        print(f"   Details: {details}")
    test_results.append({
        'test': test_name,
        'success': success,
        'details': details
    })

def make_request(method, endpoint, data=None, params=None):
    """Make HTTP request with error handling"""
    url = f"{API_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=15)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=15)
        elif method == "PATCH":
            response = requests.patch(url, json=data, timeout=15)
        elif method == "DELETE":
            response = requests.delete(url, timeout=15)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return response
    except requests.exceptions.Timeout:
        print(f"Request timed out: {method} {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def test_general_endpoints():
    """Test general API endpoints"""
    print("\n=== Testing General Endpoints ===")
    
    # Test root endpoint
    response = make_request("GET", "/")
    if response and response.status_code == 200:
        data = response.json()
        if data.get("message") == "Hello World":
            log_test("GET /api/ returns Hello World", True)
        else:
            log_test("GET /api/ returns Hello World", False, f"Got: {data}")
    else:
        log_test("GET /api/ returns Hello World", False, f"Status: {response.status_code if response else 'No response'}")

def test_blogs():
    """Test blog CRUD operations"""
    print("\n=== Testing Blog Endpoints ===")
    
    # Test POST /api/blogs
    blog_data = {
        "title": "Test Blog Post for API Testing",
        "excerpt": "This is a test blog post created during API testing",
        "tags": ["testing", "api", "backend"],
        "author": "Test Author"
    }
    
    response = make_request("POST", "/blogs", blog_data)
    if response and response.status_code == 200:
        data = response.json()
        if data.get("id") and data.get("title") == blog_data["title"]:
            created_ids['blog'] = data["id"]
            log_test("POST /api/blogs creates blog", True, f"Created blog with ID: {data['id']}")
        else:
            log_test("POST /api/blogs creates blog", False, f"Response: {data}")
    else:
        log_test("POST /api/blogs creates blog", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test GET /api/blogs
    response = make_request("GET", "/blogs")
    if response and response.status_code == 200:
        data = response.json()
        if "items" in data and isinstance(data["items"], list):
            # Check if our created blog is in the list
            found_blog = any(item.get("id") == created_ids['blog'] for item in data["items"])
            log_test("GET /api/blogs returns items array", True, f"Found {len(data['items'])} blogs, includes created: {found_blog}")
        else:
            log_test("GET /api/blogs returns items array", False, f"Response: {data}")
    else:
        log_test("GET /api/blogs returns items array", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test GET /api/blogs with search
    response = make_request("GET", "/blogs", params={"search": "Test Blog"})
    if response and response.status_code == 200:
        data = response.json()
        if "items" in data:
            found_blog = any("Test Blog" in item.get("title", "") for item in data["items"])
            log_test("GET /api/blogs?search= filters correctly", found_blog, f"Found {len(data['items'])} results")
        else:
            log_test("GET /api/blogs?search= filters correctly", False, f"Response: {data}")
    else:
        log_test("GET /api/blogs?search= filters correctly", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test PATCH /api/blogs/{id}
    if created_ids['blog']:
        update_data = {"title": "Updated Test Blog Post"}
        response = make_request("PATCH", f"/blogs/{created_ids['blog']}", update_data)
        if response and response.status_code == 200:
            data = response.json()
            if data.get("title") == "Updated Test Blog Post":
                log_test("PATCH /api/blogs/{id} updates blog", True)
            else:
                log_test("PATCH /api/blogs/{id} updates blog", False, f"Title not updated: {data.get('title')}")
        else:
            log_test("PATCH /api/blogs/{id} updates blog", False, f"Status: {response.status_code if response else 'No response'}")
        
        # Test GET /api/blogs/{id} after update
        response = make_request("GET", f"/blogs/{created_ids['blog']}")
        if response and response.status_code == 200:
            data = response.json()
            if data.get("title") == "Updated Test Blog Post":
                log_test("GET /api/blogs/{id} returns updated object", True)
            else:
                log_test("GET /api/blogs/{id} returns updated object", False, f"Title: {data.get('title')}")
        else:
            log_test("GET /api/blogs/{id} returns updated object", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test DELETE /api/blogs/{id}
    if created_ids['blog']:
        response = make_request("DELETE", f"/blogs/{created_ids['blog']}")
        if response and response.status_code == 200:
            data = response.json()
            if data.get("ok") is True:
                log_test("DELETE /api/blogs/{id} returns ok:true", True)
                
                # Test subsequent GET returns 404
                response = make_request("GET", f"/blogs/{created_ids['blog']}")
                if response and response.status_code == 404:
                    log_test("GET deleted blog returns 404", True)
                else:
                    log_test("GET deleted blog returns 404", False, f"Status: {response.status_code if response else 'No response'}")
            else:
                log_test("DELETE /api/blogs/{id} returns ok:true", False, f"Response: {data}")
        else:
            log_test("DELETE /api/blogs/{id} returns ok:true", False, f"Status: {response.status_code if response else 'No response'}")

def test_tools():
    """Test tool CRUD operations"""
    print("\n=== Testing Tool Endpoints ===")
    
    # Test POST /api/tools
    tool_data = {
        "name": "Test Development Tool",
        "category": "development",
        "description": "A test tool for API testing purposes",
        "url": "https://example.com/test-tool",
        "tags": ["testing", "development"]
    }
    
    response = make_request("POST", "/tools", tool_data)
    if response and response.status_code == 200:
        data = response.json()
        if data.get("id") and data.get("name") == tool_data["name"]:
            created_ids['tool'] = data["id"]
            log_test("POST /api/tools creates tool", True, f"Created tool with ID: {data['id']}")
        else:
            log_test("POST /api/tools creates tool", False, f"Response: {data}")
    else:
        log_test("POST /api/tools creates tool", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test GET /api/tools with category filter
    response = make_request("GET", "/tools", params={"category": "development"})
    if response and response.status_code == 200:
        data = response.json()
        if "items" in data:
            found_tool = any(item.get("category") == "development" for item in data["items"])
            log_test("GET /api/tools?category= filters correctly", found_tool, f"Found {len(data['items'])} development tools")
        else:
            log_test("GET /api/tools?category= filters correctly", False, f"Response: {data}")
    else:
        log_test("GET /api/tools?category= filters correctly", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test GET /api/tools with sort=name
    response = make_request("GET", "/tools", params={"sort": "name"})
    if response and response.status_code == 200:
        data = response.json()
        if "items" in data:
            log_test("GET /api/tools?sort=name works", True, f"Returned {len(data['items'])} tools sorted by name")
        else:
            log_test("GET /api/tools?sort=name works", False, f"Response: {data}")
    else:
        log_test("GET /api/tools?sort=name works", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test GET /api/tools with sort=category
    response = make_request("GET", "/tools", params={"sort": "category"})
    if response and response.status_code == 200:
        data = response.json()
        if "items" in data:
            log_test("GET /api/tools?sort=category works", True, f"Returned {len(data['items'])} tools sorted by category")
        else:
            log_test("GET /api/tools?sort=category works", False, f"Response: {data}")
    else:
        log_test("GET /api/tools?sort=category works", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test PATCH /api/tools/{id}
    if created_ids['tool']:
        update_data = {"name": "Updated Test Tool"}
        response = make_request("PATCH", f"/tools/{created_ids['tool']}", update_data)
        if response and response.status_code == 200:
            data = response.json()
            if data.get("name") == "Updated Test Tool":
                log_test("PATCH /api/tools/{id} updates tool", True)
            else:
                log_test("PATCH /api/tools/{id} updates tool", False, f"Name not updated: {data.get('name')}")
        else:
            log_test("PATCH /api/tools/{id} updates tool", False, f"Status: {response.status_code if response else 'No response'}")
        
        # Test GET /api/tools/{id} after update
        response = make_request("GET", f"/tools/{created_ids['tool']}")
        if response and response.status_code == 200:
            data = response.json()
            if data.get("name") == "Updated Test Tool":
                log_test("GET /api/tools/{id} returns updated object", True)
            else:
                log_test("GET /api/tools/{id} returns updated object", False, f"Name: {data.get('name')}")
        else:
            log_test("GET /api/tools/{id} returns updated object", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test DELETE /api/tools/{id}
    if created_ids['tool']:
        response = make_request("DELETE", f"/tools/{created_ids['tool']}")
        if response and response.status_code == 200:
            data = response.json()
            if data.get("ok") is True:
                log_test("DELETE /api/tools/{id} returns ok:true", True)
            else:
                log_test("DELETE /api/tools/{id} returns ok:true", False, f"Response: {data}")
        else:
            log_test("DELETE /api/tools/{id} returns ok:true", False, f"Status: {response.status_code if response else 'No response'}")

def test_path():
    """Test path CRUD operations"""
    print("\n=== Testing Path Endpoints ===")
    
    # Test POST /api/path
    path_data = {
        "label": "Test Learning Step",
        "durationMin": 30
    }
    
    response = make_request("POST", "/path", path_data)
    if response and response.status_code == 200:
        data = response.json()
        if data.get("id") and data.get("label") == path_data["label"]:
            created_ids['path'] = data["id"]
            log_test("POST /api/path creates path step", True, f"Created path step with ID: {data['id']}")
        else:
            log_test("POST /api/path creates path step", False, f"Response: {data}")
    else:
        log_test("POST /api/path creates path step", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test GET /api/path
    response = make_request("GET", "/path")
    if response and response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            found_step = any(item.get("id") == created_ids['path'] for item in data)
            log_test("GET /api/path returns list with created step", found_step, f"Found {len(data)} path steps")
        else:
            log_test("GET /api/path returns list with created step", False, f"Response: {data}")
    else:
        log_test("GET /api/path returns list with created step", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test PATCH /api/path/{id}
    if created_ids['path']:
        update_data = {"label": "Updated Learning Step"}
        response = make_request("PATCH", f"/path/{created_ids['path']}", update_data)
        if response and response.status_code == 200:
            data = response.json()
            if data.get("label") == "Updated Learning Step":
                log_test("PATCH /api/path/{id} updates step", True)
            else:
                log_test("PATCH /api/path/{id} updates step", False, f"Label not updated: {data.get('label')}")
        else:
            log_test("PATCH /api/path/{id} updates step", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test DELETE /api/path/{id}
    if created_ids['path']:
        response = make_request("DELETE", f"/path/{created_ids['path']}")
        if response and response.status_code == 200:
            data = response.json()
            if data.get("ok") is True:
                log_test("DELETE /api/path/{id} returns ok:true", True)
            else:
                log_test("DELETE /api/path/{id} returns ok:true", False, f"Response: {data}")
        else:
            log_test("DELETE /api/path/{id} returns ok:true", False, f"Status: {response.status_code if response else 'No response'}")

def test_community():
    """Test community endpoints"""
    print("\n=== Testing Community Endpoints ===")
    
    # Test POST /api/community/channels
    channel_data = {
        "name": "#general-test"
    }
    
    response = make_request("POST", "/community/channels", channel_data)
    if response and response.status_code == 200:
        data = response.json()
        if data.get("id") and data.get("name") == channel_data["name"]:
            created_ids['channel'] = data["id"]
            log_test("POST /api/community/channels creates channel", True, f"Created channel: {data['name']}")
        else:
            log_test("POST /api/community/channels creates channel", False, f"Response: {data}")
    else:
        log_test("POST /api/community/channels creates channel", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test GET /api/community/channels
    response = make_request("GET", "/community/channels")
    if response and response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            found_channel = any(item.get("name") == "#general-test" for item in data)
            log_test("GET /api/community/channels includes created channel", found_channel, f"Found {len(data)} channels")
        else:
            log_test("GET /api/community/channels includes created channel", False, f"Response: {data}")
    else:
        log_test("GET /api/community/channels includes created channel", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test POST /api/community/messages
    message_data = {
        "channel": "#general-test",
        "author": "Test User",
        "text": "This is a test message for API testing"
    }
    
    response = make_request("POST", "/community/messages", message_data)
    if response and response.status_code == 200:
        data = response.json()
        if data.get("id") and data.get("channel") == message_data["channel"]:
            created_ids['message'] = data["id"]
            log_test("POST /api/community/messages creates message", True, f"Created message in {data['channel']}")
        else:
            log_test("POST /api/community/messages creates message", False, f"Response: {data}")
    else:
        log_test("POST /api/community/messages creates message", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test GET /api/community/messages with channel filter
    response = make_request("GET", "/community/messages", params={"channel": "#general-test"})
    if response and response.status_code == 200:
        data = response.json()
        if "items" in data and "page" in data and "total" in data:
            found_message = any(item.get("id") == created_ids['message'] for item in data["items"])
            log_test("GET /api/community/messages includes message with pagination", found_message, 
                    f"Found {len(data['items'])} messages, page {data['page']}, total {data['total']}")
        else:
            log_test("GET /api/community/messages includes message with pagination", False, f"Response: {data}")
    else:
        log_test("GET /api/community/messages includes message with pagination", False, f"Status: {response.status_code if response else 'No response'}")

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n=== Testing Edge Cases ===")
    
    # Test 404 on non-existing blog
    fake_id = "non-existing-id-12345"
    response = make_request("GET", f"/blogs/{fake_id}")
    if response and response.status_code == 404:
        log_test("GET non-existing blog returns 404", True)
    else:
        log_test("GET non-existing blog returns 404", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test 404 on non-existing tool
    response = make_request("GET", f"/tools/{fake_id}")
    if response and response.status_code == 404:
        log_test("GET non-existing tool returns 404", True)
    else:
        log_test("GET non-existing tool returns 404", False, f"Status: {response.status_code if response else 'No response'}")
    
    # Test 404 on non-existing path
    response = make_request("GET", f"/path/{fake_id}")
    if response:
        # Note: The path endpoint doesn't have individual GET, so this should return 404
        log_test("GET non-existing path returns 404", response.status_code == 404)
    else:
        log_test("GET non-existing path returns 404", False, "No response")
    
    # Test validation: tools sort parameter
    response = make_request("GET", "/tools", params={"sort": "invalid_sort"})
    if response and response.status_code == 422:
        log_test("GET /api/tools with invalid sort returns validation error", True)
    else:
        log_test("GET /api/tools with invalid sort returns validation error", False, f"Status: {response.status_code if response else 'No response'}")

def print_summary():
    """Print test summary"""
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for result in test_results if result['success'])
    total = len(test_results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if total - passed > 0:
        print("\nFailed Tests:")
        for result in test_results:
            if not result['success']:
                print(f"❌ {result['test']}")
                if result['details']:
                    print(f"   {result['details']}")
    
    return passed == total

def main():
    """Run all tests"""
    print("Starting Backend API Tests...")
    print(f"Backend URL: {API_URL}")
    
    try:
        test_general_endpoints()
        test_blogs()
        test_tools()
        test_path()
        test_community()
        test_edge_cases()
        
        success = print_summary()
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"Test execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()