# JSON Comparator API with React Frontend

A powerful FastAPI-based service with a modern React frontend for comparing JSON objects with detailed difference analysis, similar to Beyond Compare for JSON data.

## 🎯 **Complete Full-Stack Solution**

This project includes:
- **Backend**: FastAPI REST API for JSON comparison
- **Frontend**: Modern React web interface with drag & drop file upload
- **Full Integration**: Seamless communication between frontend and backend

## Features

### Backend API
- **Deep JSON Comparison**: Recursively compares nested JSON objects and arrays
- **Detailed Difference Reporting**: Shows exactly what changed, where it changed, and how
- **Flexible Comparison Options**: 
  - Ignore order of items in lists
  - Ignore case sensitivity for strings
- **Multiple Input Methods**: 
  - Direct JSON objects via POST
  - JSON strings via POST
  - URL-encoded JSON via GET
- **Rich API Documentation**: Interactive Swagger UI and ReDoc documentation
- **Beyond Compare-like Output**: Structured diff reporting similar to popular comparison tools

### Frontend UI
- **Modern React Interface**: Clean, intuitive web interface
- **Dual Input Methods**: Paste JSON directly or upload JSON files
- **Drag & Drop Support**: Drag JSON files directly into input areas
- **Real-time Validation**: Instant JSON syntax validation with visual feedback
- **Visual Diff Display**: Color-coded differences with detailed breakdown
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark Mode Support**: Automatic dark/light mode based on system preference
- **Export Results**: Copy or download comparison results

## Difference Types Detected

- **Added**: New fields/values in the second JSON
- **Removed**: Fields/values present in first JSON but missing in second
- **Modified**: Values that changed between the two JSONs
- **Type Changed**: Fields where the data type changed (e.g., string to number)

## 🚀 Quick Start

### Option 1: Full Stack (Frontend + Backend)

**Automated Setup:**
```bash
# Setup everything at once
setup.bat              # Windows Batch

# Start both backend and frontend  
start_fullstack.bat     # Windows Batch
```

**Manual Setup:**
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Node.js dependencies  
cd frontend
npm install
cd ..

# 3. Start backend (Terminal 1)
python main.py

# 4. Start frontend (Terminal 2)  
cd frontend
npm start
```

**Access:**
- **Frontend UI**: http://localhost:3000 (Main interface)
- **Backend API**: http://localhost:8000/docs (API documentation)

### Option 2: Backend Only

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
python main.py
```

The API will be available at `http://localhost:8000`

### 3. Access Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### POST /compare

Compare two JSON objects directly.

**Request Body:**
```json
{
  "json1": {"name": "John", "age": 30},
  "json2": {"name": "John", "age": 31},
  "ignore_order": false,
  "ignore_case": false
}
```

**Response:**
```json
{
  "total_differences": 1,
  "are_equal": false,
  "differences": [
    {
      "path": "age",
      "change_type": "modified",
      "old_value": 30,
      "new_value": 31,
      "old_type": "int",
      "new_type": "int"
    }
  ],
  "summary": {
    "added": 0,
    "removed": 0,
    "modified": 1,
    "type_changed": 0
  }
}
```

### POST /compare-text

Compare JSON provided as text strings.

**Request Body:**
```json
{
  "json_text1": "{\"name\": \"Alice\", \"age\": 25}",
  "json_text2": "{\"name\": \"Alice\", \"age\": 26}",
  "ignore_order": false,
  "ignore_case": false
}
```

### GET /compare

Compare JSON via GET request with query parameters.

```
GET /compare?json1={"name":"John"}&json2={"name":"Jane"}&ignore_order=false&ignore_case=false
```

## Usage Examples

### Using the API with Python requests

```python
import requests
import json

# Example JSON objects
json1 = {
    "user": {
        "name": "John Doe",
        "age": 30,
        "skills": ["Python", "JavaScript"]
    }
}

json2 = {
    "user": {
        "name": "John Doe", 
        "age": 31,
        "skills": ["Python", "JavaScript", "Go"]
    }
}

# Compare via API
response = requests.post("http://localhost:8000/compare", json={
    "json1": json1,
    "json2": json2,
    "ignore_order": False,
    "ignore_case": False
})

result = response.json()
print(f"Total differences: {result['total_differences']}")
for diff in result['differences']:
    print(f"{diff['path']}: {diff['change_type']}")
```

### Using the Library Directly

```python
from json_comparator import compare_json_objects

result = compare_json_objects(json1, json2)
print(f"Are equal: {result['are_equal']}")
print(f"Differences: {result['total_differences']}")
```

### Using curl

```bash
# Compare JSON objects
curl -X POST "http://localhost:8000/compare" \
     -H "Content-Type: application/json" \
     -d '{
       "json1": {"name": "John", "age": 30},
       "json2": {"name": "John", "age": 31}
     }'
```

## Comparison Options

### ignore_order (boolean, default: false)
When `true`, ignores the order of items in arrays.

```json
// With ignore_order=false, these are different:
{"items": [1, 2, 3]} vs {"items": [3, 2, 1]}

// With ignore_order=true, these are considered equal:
{"items": [1, 2, 3]} vs {"items": [3, 2, 1]}
```

### ignore_case (boolean, default: false)
When `true`, ignores case when comparing strings.

```json
// With ignore_case=false, these are different:
{"name": "John"} vs {"name": "JOHN"}

// With ignore_case=true, these are considered equal:
{"name": "John"} vs {"name": "JOHN"}
```

## Response Format

The API returns a standardized response with the following structure:

- **total_differences**: Total number of differences found
- **are_equal**: Boolean indicating if the objects are identical
- **differences**: Array of detailed difference objects
- **summary**: Count of each type of difference

### Difference Object Structure

```json
{
  "path": "user.address.city",
  "change_type": "modified",
  "old_value": "New York",
  "new_value": "Boston",
  "old_type": "str",
  "new_type": "str"
}
```

- **path**: JSON path to the changed field (dot notation for objects, brackets for arrays)
- **change_type**: Type of change (added, removed, modified, type_changed)
- **old_value**: Original value (for removed/modified changes)
- **new_value**: New value (for added/modified changes)  
- **old_type**/**new_type**: Data types of the values

## Real-World Examples

### Comparing User Profiles

```python
# Before update
user_before = {
    "id": 123,
    "profile": {
        "name": "John Doe",
        "email": "john@old-company.com",
        "settings": {
            "theme": "dark",
            "notifications": True
        }
    },
    "roles": ["user"]
}

# After update  
user_after = {
    "id": 123,
    "profile": {
        "name": "John Doe",
        "email": "john@new-company.com", 
        "phone": "+1-555-0123",  # Added
        "settings": {
            "theme": "light",  # Modified
            "notifications": True,
            "language": "en"  # Added
        }
    },
    "roles": ["user", "admin"]  # Added role
}

# Compare to see what changed
result = compare_json_objects(user_before, user_after)
# Will show email change, theme change, added phone, added language, added role
```

### Comparing API Responses

```python
# Compare API responses to detect changes
old_api_response = {
    "data": {
        "products": [
            {"id": 1, "name": "Widget A", "price": 19.99},
            {"id": 2, "name": "Widget B", "price": 29.99}
        ],
        "total": 2
    }
}

new_api_response = {
    "data": {
        "products": [
            {"id": 1, "name": "Widget A", "price": 21.99},  # Price changed
            {"id": 2, "name": "Widget B", "price": 29.99},
            {"id": 3, "name": "Widget C", "price": 39.99}   # New product
        ],
        "total": 3  # Updated count
    }
}

result = compare_json_objects(old_api_response, new_api_response)
# Will detect price change and new product addition
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **400 Bad Request**: Invalid JSON format or comparison errors
- **422 Unprocessable Entity**: Invalid request payload structure
- **500 Internal Server Error**: Unexpected server errors

Example error response:
```json
{
  "detail": "Invalid JSON format: Expecting ',' delimiter: line 2 column 15 (char 16)"
}
```

## Performance Considerations

- The API can handle moderately large JSON objects efficiently
- Deep nesting and large arrays may impact performance
- Consider chunking very large datasets for comparison

## Development

### Project Structure

```
FastAPI/
├── main.py              # FastAPI application
├── json_comparator.py   # Core comparison logic
├── examples.py          # Usage examples
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Running Tests

```bash
# Run the examples
python examples.py

# Test the API (server must be running)
python -c "import examples; examples.demo_api_usage()"
```

### Dependencies

- **FastAPI**: Web framework for building the API
- **Uvicorn**: ASGI server for running the application
- **Pydantic**: Data validation and parsing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License.