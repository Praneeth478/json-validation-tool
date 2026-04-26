"""
Example usage of the JSON Comparator API.
This file demonstrates how to use the API both as a library and via HTTP requests.
"""

import json
import requests
from json_comparator import compare_json_objects


# Example JSON objects for comparison
json_obj1 = {
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "is_active": True,
        "skills": ["Python", "JavaScript", "SQL"],
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "zipcode": "10001",
            "country": "USA"
        },
        "preferences": {
            "theme": "dark",
            "notifications": True
        }
    },
    "metadata": {
        "created_at": "2023-01-15",
        "updated_at": "2023-01-15"
    }
}

json_obj2 = {
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",  # Changed email
        "age": 31,  # Changed age
        "is_active": True,
        "skills": ["Python", "JavaScript", "SQL", "Go"],  # Added skill
        "address": {
            "street": "456 Oak Ave",  # Changed street
            "city": "Boston",  # Changed city
            "zipcode": "02101",  # Changed zipcode
            "country": "USA",
            "state": "MA"  # Added state
        },
        "preferences": {
            "theme": "light",  # Changed theme
            "notifications": True,
            "language": "en"  # Added language
        }
    },
    "metadata": {
        "created_at": "2023-01-15",
        "updated_at": "2023-03-20"  # Changed update date
    }
}


def demo_library_usage():
    """Demonstrate using the comparison library directly."""
    print("=== Direct Library Usage ===")
    
    result = compare_json_objects(json_obj1, json_obj2)
    
    print(f"Total differences: {result['total_differences']}")
    print(f"Are equal: {result['are_equal']}")
    print(f"Summary: {result['summary']}")
    print("\nDifferences:")
    
    for diff in result['differences']:
        print(f"  - {diff['path']}: {diff['change_type']}")
        if diff['change_type'] == 'modified':
            print(f"    Old: {diff['old_value']} -> New: {diff['new_value']}")
        elif diff['change_type'] == 'added':
            print(f"    Added: {diff['new_value']}")
        elif diff['change_type'] == 'removed':
            print(f"    Removed: {diff['old_value']}")
    
    print("\n" + "="*50 + "\n")


def demo_api_usage():
    """Demonstrate using the API via HTTP requests."""
    print("=== API Usage Examples ===")
    
    # First start the server by running: python main.py
    # Then uncomment and run these examples
    
    api_url = "http://localhost:8000"
    
    # Example 1: Compare via POST request
    print("1. Comparing via POST /compare")
    payload = {
        "json1": json_obj1,
        "json2": json_obj2,
        "ignore_order": False,
        "ignore_case": False
    }
    
    try:
        response = requests.post(f"{api_url}/compare", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"   Total differences: {result['total_differences']}")
            print(f"   Summary: {result['summary']}")
        else:
            print(f"   API request failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   API server is not running. Start it with: python main.py")
    
    # Example 2: Compare JSON strings
    print("\n2. Comparing JSON strings via POST /compare-text")
    text_payload = {
        "json_text1": json.dumps({"name": "Alice", "age": 25}),
        "json_text2": json.dumps({"name": "Alice", "age": 26}),
        "ignore_order": False,
        "ignore_case": False
    }
    
    try:
        response = requests.post(f"{api_url}/compare-text", json=text_payload)
        if response.status_code == 200:
            result = response.json()
            print(f"   Total differences: {result['total_differences']}")
            print(f"   Differences: {result['differences']}")
        else:
            print(f"   API request failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   API server is not running. Start it with: python main.py")
    
    print("\n" + "="*50 + "\n")


def demo_comparison_options():
    """Demonstrate different comparison options."""
    print("=== Comparison Options Demo ===")
    
    # Demo with different options
    list_obj1 = {"items": [1, 2, 3], "text": "Hello"}
    list_obj2 = {"items": [3, 2, 1], "text": "HELLO"}
    
    print("Comparing with order sensitivity:")
    result1 = compare_json_objects(list_obj1, list_obj2, ignore_order=False, ignore_case=False)
    print(f"  Differences: {result1['total_differences']}")
    
    print("\nComparing ignoring order:")
    result2 = compare_json_objects(list_obj1, list_obj2, ignore_order=True, ignore_case=False)
    print(f"  Differences: {result2['total_differences']}")
    
    print("\nComparing ignoring order and case:")
    result3 = compare_json_objects(list_obj1, list_obj2, ignore_order=True, ignore_case=True)
    print(f"  Differences: {result3['total_differences']}")
    
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    print("JSON Comparator API - Usage Examples\n")
    
    # Run library demos
    demo_library_usage()
    demo_comparison_options()
    
    # API demo (requires server to be running)
    demo_api_usage()
    
    print("To start the API server, run:")
    print("  python main.py")
    print("\nThen visit:")
    print("  http://localhost:8000/docs - Interactive API documentation")
    print("  http://localhost:8000/redoc - Alternative documentation")