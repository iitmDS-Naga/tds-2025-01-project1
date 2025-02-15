import httpx
import json
import os

def task_fetch_data_from_api(api_url, http_method='GET', output_file_path=None, 
                            request_headers=None, request_params=None):
    """
    Fetches data from an API and saves it to a file.
    
    Args:
        api_url (str): URL of the API endpoint
        http_method (str): HTTP method to use (default: 'GET')
        output_file_path (str): Path where the API response should be saved
        request_headers (dict): Headers to include in the API request
        request_params (dict): Query parameters for the API request
    
    Returns:
        dict: API response data
    """
    try:
        # Set default values if None
        request_headers = request_headers or {}
        request_params = request_params or {}
        
        # Make the API request using a client context manager
        with httpx.Client() as client:
            response = client.request(
                method=http_method,
                url=api_url,
                headers=request_headers,
                params=request_params
            )
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
        
        # Save to file if output path is provided
        if output_file_path:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            
            # Write the data to file
            with open(output_file_path, 'w') as f:
                json.dump(data, f, indent=2)
        
        return data
        
    except httpx.RequestError as e:
        print(f"Error making API request: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        raise
    except IOError as e:
        print(f"Error writing to file: {e}")
        raise