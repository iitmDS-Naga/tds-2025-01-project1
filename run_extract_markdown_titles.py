import os
import glob
import json
from typing import Dict, Any
import re

async def run_extract_markdown_titles(
    input_directory: str,
    output_file_path: str,
    file_pattern: str,
    tag_pattern: str = "#"
) -> Dict[str, Any]:
    try:
        # Validate input directory path
        if not input_directory.startswith("/data/"):
            return {
                "status": "error",
                "message": "Input directory must start with '/data/'"
            }

        # Ensure input directory exists
        full_input_path = os.path.join("..", input_directory)
        if not os.path.exists(full_input_path):
            return {
                "status": "error",
                "message": f"Input directory not found: {input_directory}"
            }

        # Get list of markdown files matching pattern recursively
        search_pattern = os.path.join(full_input_path, "**", file_pattern)
        md_files = glob.glob(search_pattern, recursive=True)

        if not md_files:
            return {
                "status": "error",
                "message": f"No markdown files found matching pattern: {file_pattern}"
            }

        # Dictionary to store file paths and their titles
        markdown_index = {}

        # Process each markdown file
        for file_path in md_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                    # Extract first level 1 heading (# Title)
                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    
                    # If no level 1 heading, try to get first heading of any level
                    if not title_match:
                        title_match = re.search(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)

                    # Use filename as title if no heading found
                    if title_match:
                        title = title_match.group(1).strip()
                    else:
                        title = os.path.splitext(os.path.basename(file_path))[0]

                    # Store relative path from /data/ directory
                    rel_path = os.path.relpath(file_path, os.path.join("..", "data"))
                    markdown_index[rel_path] = title

            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Error processing file {file_path}: {str(e)}"
                }

        # Write index to output file
        full_output_path = os.path.join("..", output_file_path)
        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)
        
        with open(full_output_path, 'w') as f:
            json.dump(markdown_index, f, indent=2)

        return {
            "status": "success",
            "message": f"Successfully created index with {len(markdown_index)} entries in {output_file_path}",
            "files_processed": len(markdown_index)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing request: {str(e)}"
        }
