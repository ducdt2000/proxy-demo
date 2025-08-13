#!/usr/bin/env python3
"""
Test script to demonstrate X-Next-Services header functionality
"""
import requests
import time

def test_proxy_with_x_next_services():
    """Test the proxy with X-Next-Services routing"""
    proxy_url = "http://localhost:3128"
    test_url = "http://httpbin.org/get"
    
    # Configure proxy
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    
    print("Testing X-Next-Services header functionality...")
    print("=" * 50)
    
    for i in range(3):
        print(f"\nTest request #{i+1}")
        try:
            response = requests.get(test_url, proxies=proxies, timeout=30)
            print(f"Status: {response.status_code}")
            print(f"Response size: {len(response.content)} bytes")
            print(f"Response headers: {response.headers}")
            
            # Check if request was successful
            if response.status_code == 200:
                print("✓ Request successful - check ICAP server logs for X-Next-Services routing")
            else:
                print(f"✗ Request failed with status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Request failed: {e}")
        
        time.sleep(2)  # Wait between requests
    
    print("\n" + "=" * 50)
    print("Test completed. Check the Docker logs to see:")
    print("1. Health checks being performed")
    print("2. X-Next-Services headers being added")
    print("3. Dynamic service routing in action")
    print("\nTo view logs: docker-compose logs icap-server icap-server2")

if __name__ == "__main__":
    test_proxy_with_x_next_services()
