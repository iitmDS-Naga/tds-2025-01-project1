import os
import httpx
from pathlib import Path
import base64

async def run_extract_card_number(
    input_image_path="/data/credit-card.png",
    output_file_path="/data/credit-card.txt",
    process_instruction="extract card number without spaces"
):
    try:
        # Ensure input file exists
        if not os.path.exists(input_image_path):
            raise FileNotFoundError(f"Input image not found: {input_image_path}")
            
        # Read image file as base64
        with open(input_image_path, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

        # Retrieve API token
        proxy_token = os.getenv('AIPROXY_TOKEN')
        if not proxy_token:
            raise ValueError("AIPROXY_TOKEN not found in environment variables")

        headers = {
            "Authorization": f"Bearer {proxy_token}",
            "Content-Type": "application/json"
        }

        # Create prompt for GPT-4V
        prompt = f"{process_instruction} from the given image"
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
            {
                "role": "user",
                "content": prompt,
                "image": f"data:image/png;base64,{img_base64}"
            }
            ],
            "max_tokens": 300
        }

        # Call the API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()

        # Extract the processed result
        result = data["choices"][0]["message"]["content"].strip()
        
        # Remove any non-digit characters
        card_number = ''.join(filter(str.isdigit, result))

        # Create output directory if needed
        output_dir = os.path.dirname(output_file_path)
        if output_dir:
            Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Write card number to output file
        with open(output_file_path, 'w') as file:
            file.write(card_number)

        return {
            "status": "success",
            "message": f"Card number extracted and written to {output_file_path}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }