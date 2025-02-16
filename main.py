from typing import Dict, Any

from fastapi import FastAPI, Request, Response
from openai import OpenAI
from pathlib import Path
import json
import os
import httpx

from custom_function import custom_function
from run_datagen import run_datagen
from run_prettier_format import run_prettier_format
from run_count_days import run_count_days
from run_sort_array_of_contacts import run_sort_array_of_contacts
from run_write_most_recent_logs import run_write_most_recent_logs
from run_extract_markdown_titles import run_extract_markdown_titles
from task_fetch_data_from_api import task_fetch_data_from_api
from task_extract_data_from_website import task_extract_data_from_website
from run_extract_on_email import run_extract_on_email
from run_extract_card_number import run_extract_card_number
app = FastAPI()

async def parse_task(task_description: str) -> Dict[str, Any]:
    """Parse task description into structured JSON plan using GPT-4."""
    headers = {
        "Authorization": f"Bearer {os.getenv('AIPROXY_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{
            "role": "user",
            "content": task_description
        }],
        "functions": custom_function,
        "function_call": "auto"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
    
    response_message = data["choices"][0]["message"]
    
    if "function_call" not in response_message:
        raise ValueError("No function call returned by GPT-4")

    response_dict = {
        response_message["function_call"]["name"]: 
        json.loads(response_message["function_call"]["arguments"])
    }
    return response_dict

async def call_task(task_object: Dict[str,Any]):
    # T-35 Implement plan execution logic
    # Which function call was invoked
    function_called = list(task_object.keys())[0]
    function_args = task_object[function_called]

    print(function_args)
    # Function names need to finish run_datagen
    available_functions = {
        "run_datagen": run_datagen,
        "run_prettier_format": run_prettier_format,
        "run_count_days": run_count_days,
        "run_sort_array_of_contacts": run_sort_array_of_contacts,
        "run_write_most_recent_logs": run_write_most_recent_logs,
        "run_extract_markdown_titles": run_extract_markdown_titles,
        "task_fetch_data_from_api": task_fetch_data_from_api,
        "task_extract_data_from_website": task_extract_data_from_website,
        "run_extract_on_email": run_extract_on_email,
        "run_extract_card_number": run_extract_card_number
    }
    
    function_to_call = available_functions[function_called]

    print("\033[91m", function_to_call, "\033[0m")  # Print in red using ANSI escape codes
    task_response = await function_to_call(*list(function_args.values()))
    # Extracting the arguments
    # function_args  = json.loads(response_message.function_call.arguments)
    
    print(task_response)

    return task_response


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint returning a welcome message."""
    return {"message": "Hello from tds-2025-01-project1!"}


@app.post("/run")
async def run_task(request: Request) -> Response:
    """Execute a task based on the provided description."""
    task = request.query_params.get('task')
    if not task:
        return Response(content="Task is required", status_code=400)
    
    try:
        plan = await parse_task(task)
        print(plan)
        action_response = await call_task(plan)
        print(action_response)
        return Response(content=json.dumps(action_response), status_code=200)
    except Exception as e:
        return Response(content=f"Task parsing failed: {str(e)}", status_code=400)
    
@app.get("/read")
async def read_file(path: str = None) -> Response:
    """Read and return contents of specified file from data directory."""
    if not path:
        return Response(content="Path parameter is required", status_code=400)
    
    try:
        clean_path = path.replace('/data/', '').lstrip('/')
        # Construct path and resolve to absolute path
        data_dir = Path("../data").resolve()
        file_path = (data_dir / clean_path).resolve()
        
        # Verify the path is within data directory
        if not str(file_path).startswith(str(data_dir)):
            return Response(
                content="Access denied: Can only access files in data directory",
                status_code=403
            )
            
        if not file_path.is_file():
            return Response(status_code=404)
            
        with open(file_path, 'r') as file:
            content = file.read()
        return Response(content=content, status_code=200)
    
    except Exception as e:
        return Response(
            content=f"Error reading file: {str(e)}", 
            status_code=500
        )