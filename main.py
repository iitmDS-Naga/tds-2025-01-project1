from typing import Dict, Any

from fastapi import FastAPI, Request, Response
from openai import OpenAI
import json
import os
import subprocess

from custom_function import custom_function
from run_datagen import run_datagen
from run_prettier_format import run_prettier_format
from run_count_days import run_count_days

app = FastAPI()


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def parse_task(task_description: str) -> Dict[str, Any]:
    """Parse task description into structured JSON plan using GPT-4."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": task_description
        }],
        functions= custom_function,
        function_call="auto"
    )
    
    response_message = response.choices[0].message

    if response_message.function_call is None:
        raise ValueError("No function call returned by GPT-4")

    response_dict = { response_message.function_call.name : json.loads(response_message.function_call.arguments)}
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
        "run_count_days": run_count_days

    }
    
    function_to_call = available_functions[function_called]

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
        plan = parse_task(task)
        print(plan)
        action_response = await call_task(plan)
        print(action_response)
        return Response(content=json.dumps(action_response), status_code=200)
    except Exception as e:
        return Response(content=f"Task parsing failed: {str(e)}", status_code=400)
    
@app.get("/read")
async def read_file(path: str = None) -> Response:
    """Read and return contents of specified file."""
    if not path:
        return Response(content="Path parameter is required", status_code=400)
    try:
        with open(f"../{path}", 'r') as file:
            content = file.read()
        return Response(content=content, status_code=200)
    except FileNotFoundError:
        return Response(status_code=404)