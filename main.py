"""
FastAPI application for JSON comparison service.
Provides REST API endpoints to compare JSON objects similar to Beyond Compare.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Dict, Optional
import json
import uvicorn

from json_comparator import compare_json_objects


# Pydantic models for request/response
class JSONCompareRequest(BaseModel):
    """Request model for JSON comparison."""
    json1: Any = Field(..., description="First JSON object to compare")
    json2: Any = Field(..., description="Second JSON object to compare")
    ignore_order: Optional[bool] = Field(False, description="Ignore order of items in lists")
    ignore_case: Optional[bool] = Field(False, description="Ignore case when comparing strings")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "json1": {
                    "name": "John Doe",
                    "age": 30,
                    "skills": ["Python", "JavaScript"],
                    "address": {
                        "city": "New York",
                        "zipcode": "10001"
                    }
                },
                "json2": {
                    "name": "John Doe",
                    "age": 31,
                    "skills": ["Python", "JavaScript", "Go"],
                    "address": {
                        "city": "Boston",
                        "zipcode": "02101"
                    }
                },
                "ignore_order": False,
                "ignore_case": False
            }
        }
    )


class JSONCompareResponse(BaseModel):
    """Response model for JSON comparison."""
    total_differences: int = Field(..., description="Total number of differences found")
    are_equal: bool = Field(..., description="Whether the JSON objects are equal")
    differences: list = Field(..., description="List of detailed differences")
    summary: Dict[str, int] = Field(..., description="Summary of difference types")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_differences": 3,
                "are_equal": False,
                "differences": [
                    {
                        "path": "age",
                        "change_type": "modified",
                        "old_value": 30,
                        "new_value": 31,
                        "old_type": "int",
                        "new_type": "int"
                    },
                    {
                        "path": "skills[2]",
                        "change_type": "added",
                        "new_value": "Go",
                        "new_type": "str"
                    },
                    {
                        "path": "address.city",
                        "change_type": "modified",
                        "old_value": "New York",
                        "new_value": "Boston",
                        "old_type": "str",
                        "new_type": "str"
                    }
                ],
                "summary": {
                    "added": 1,
                    "removed": 0,
                    "modified": 2,
                    "type_changed": 0
                }
            }
        }
    )


class JSONCompareFromTextRequest(BaseModel):
    """Request model for comparing JSON from text strings."""
    json_text1: str = Field(..., description="First JSON as text string")
    json_text2: str = Field(..., description="Second JSON as text string")
    ignore_order: Optional[bool] = Field(False, description="Ignore order of items in lists")
    ignore_case: Optional[bool] = Field(False, description="Ignore case when comparing strings")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "json_text1": '{"name": "Alice", "age": 25}',
                "json_text2": '{"name": "Alice", "age": 26}',
                "ignore_order": False,
                "ignore_case": False
            }
        }
    )


# Initialize FastAPI app
app = FastAPI(
    title="JSON Comparator API",
    description="A powerful API for comparing JSON objects with detailed difference analysis, similar to Beyond Compare",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "JSON Comparator API",
        "description": "Compare JSON objects and get detailed differences",
        "endpoints": {
            "compare": "/compare - Compare two JSON objects",
            "compare-text": "/compare-text - Compare JSON from text strings",
            "docs": "/docs - Interactive API documentation",
            "health": "/health - Health check endpoint"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "JSON Comparator API"}


@app.post("/compare", response_model=JSONCompareResponse)
async def compare_json(request: JSONCompareRequest):
    """
    Compare two JSON objects and return detailed differences.
    
    This endpoint compares two JSON objects and returns:
    - Total number of differences
    - Whether objects are equal
    - Detailed list of differences with paths
    - Summary of difference types
    
    The comparison supports options to ignore order in lists and case in strings.
    """
    try:
        result = compare_json_objects(
            request.json1,
            request.json2,
            ignore_order=request.ignore_order,
            ignore_case=request.ignore_case
        )
        return JSONCompareResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error comparing JSON objects: {str(e)}")


@app.post("/compare-text", response_model=JSONCompareResponse)
async def compare_json_from_text(request: JSONCompareFromTextRequest):
    """
    Compare JSON objects provided as text strings.
    
    This endpoint accepts JSON as text strings, parses them, and compares the resulting objects.
    Useful when you have JSON data as strings that need to be compared.
    """
    try:
        # Parse JSON strings
        json1 = json.loads(request.json_text1)
        json2 = json.loads(request.json_text2)
        
        # Compare the parsed objects
        result = compare_json_objects(
            json1,
            json2,
            ignore_order=request.ignore_order,
            ignore_case=request.ignore_case
        )
        return JSONCompareResponse(**result)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error comparing JSON objects: {str(e)}")


@app.get("/compare")
async def compare_json_get(
    json1: str = Query(..., description="First JSON object as URL-encoded string"),
    json2: str = Query(..., description="Second JSON object as URL-encoded string"),
    ignore_order: bool = Query(False, description="Ignore order of items in lists"),
    ignore_case: bool = Query(False, description="Ignore case when comparing strings")
):
    """
    Compare JSON objects via GET request with query parameters.
    
    This endpoint allows comparison via GET request where JSON objects are passed
    as URL-encoded strings in query parameters. Useful for simple comparisons
    or when POST requests are not preferred.
    """
    try:
        # Parse JSON strings from query parameters
        obj1 = json.loads(json1)
        obj2 = json.loads(json2)
        
        # Compare the parsed objects
        result = compare_json_objects(
            obj1,
            obj2,
            ignore_order=ignore_order,
            ignore_case=ignore_case
        )
        return result
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format in query parameters: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error comparing JSON objects: {str(e)}")


if __name__ == "__main__":
    print("Starting JSON Comparator API...")
    print("API Documentation will be available at: http://localhost:8000/docs")
    print("Interactive documentation at: http://localhost:8000/redoc")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )