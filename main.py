from typing import Dict, Any

from fastapi import FastAPI, Request, Response
from openai import OpenAI
import json
import os
import subprocess

app = FastAPI()

DATA_DIR = '/data'
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def parse_task(task_description: str) -> Dict[str, Any]:
    """Parse task description into structured JSON plan using GPT-4."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "system",
            "content": """Parse the task into a JSON plan with possible actions: 
                      run_command, read_file, write_file, call_llm, process_data, 
                      process_image, sql_query. Include necessary parameters."""
        }, {
            "role": "user",
            "content": task_description
        }],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


def execute_command(command: str) -> str:
    """Execute a shell command safely and return its output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise Exception(f"Command failed: {e.stderr}")


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
        # T-35 Implement plan execution logic
        return Response(content="Task parsed successfully", status_code=200)
    except Exception as e:
        return Response(content=f"Task parsing failed: {str(e)}", status_code=400)