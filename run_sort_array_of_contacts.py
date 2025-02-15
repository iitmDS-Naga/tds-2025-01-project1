import json
import os
from typing import List, Dict, Any

async def run_sort_array_of_contacts(input_file_path: str, output_file_path: str, sort_attributes: List[str]) -> Dict[str, Any]:
    """
    Sort an array of contacts based on specified attributes.

    Args:
        input_file_path (str): Path to the input JSON file containing contacts
        output_file_path (str): Path where the sorted contacts should be written
        sort_attributes (List[str]): List of attributes to sort by in order of priority

    Returns:
        Dict[str, Any]: Response dictionary containing status and message
    """
    try:
        # Check if input file exists
        if not os.path.exists("../" + input_file_path):
            return {
                "status": "error",
                "message": f"Input file not found at: {input_file_path}"
            }

        # Read the JSON file
        with open("../" + input_file_path, 'r') as file:
            contacts = json.load(file)

        # Validate input is a list
        if not isinstance(contacts, list):
            return {
                "status": "error",
                "message": "Input file must contain an array of contacts"
            }

        # Sort contacts based on multiple attributes
        try:
            sorted_contacts = sorted(
                contacts,
                key=lambda x: [str(x.get(attr, "")).lower() for attr in sort_attributes]
            )
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error sorting contacts: {str(e)}"
            }

        # Write sorted contacts to output file
        with open("../" + output_file_path, 'w') as f:
            json.dump(sorted_contacts, f, indent=2)

        return {
            "status": "success",
            "message": f"Successfully sorted contacts and wrote result to {output_file_path}",
            "count": len(sorted_contacts)
        }

    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "message": f"Invalid JSON in input file: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing request: {str(e)}"
        }