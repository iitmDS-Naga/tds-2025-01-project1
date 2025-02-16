import os
import httpx
from pathlib import Path

async def run_extract_on_email(input_file_path="/data/email.txt", 
                        output_file_path="/data/email-sender.txt",
                        process_instruction="extract sender emails"):
    try:
        # Ensure input file exists
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"Input file not found: {input_file_path}")

        # Read input file
        with open(input_file_path, 'r', encoding='utf-8') as file:
            email_text = file.read()

        # Retrieve API token
        proxy_token = os.getenv('AIPROXY_TOKEN')
        if not proxy_token:
            raise ValueError("AIPROXY_TOKEN not found in environment variables")

        headers = {
            "Authorization": f"Bearer {proxy_token}",
            "Content-Type": "application/json"
        }

        # Create prompt for GPT similar to main.py
        prompt = f"Given the following text, {process_instruction}:\n\n{email_text}"
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that processes email text."},
                {"role": "user", "content": prompt}
            ]
        }

        # Call the API using async httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()

        # Extract the processed result
        response_message = data["choices"][0]["message"]
        result = response_message.get("content", "").strip()
        if not result:
            raise ValueError("No content returned in API call.")

        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_file_path)
        if output_dir:
            Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Write results to output file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(result)

        return {
            "status": "success",
            "message": f"Results written to {output_file_path}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }