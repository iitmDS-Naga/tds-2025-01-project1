import os
import glob
from typing import Dict, Any
from datetime import datetime
import re

async def run_write_most_recent_logs(
    input_directory: str,
    file_pattern: str,
    output_file_path: str,
    num_files: int,
    lines_per_file: int
) -> Dict[str, Any]:
    """
    Write most recent log entries from multiple files to a single output file.

    Args:
        input_directory (str): Directory path containing the log files
        file_pattern (str): Pattern to match log files (*.log)
        output_file_path (str): Path where the combined log entries should be written
        num_files (int): Number of most recent log files to process
        lines_per_file (int): Number of lines to extract from each file

    Returns:
        Dict[str, Any]: Response dictionary containing status and message
    """
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

        # Get list of log files matching pattern
        search_pattern = os.path.join(full_input_path, file_pattern)
        log_files = glob.glob(search_pattern)

        if not log_files:
            return {
                "status": "error",
                "message": f"No log files found matching pattern: {file_pattern}"
            }

        # Sort files by modification time, newest first
        log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        # Take only the specified number of most recent files
        selected_files = log_files[:num_files]

        # Process each file and collect recent lines
        combined_logs = []
        for file_path in selected_files:
            try:
                with open(file_path, 'r') as f:
                    # Read all lines and take the last 'first_line_per_file' lines
                    lines = f.readlines()
                    recent_lines = lines[:1]
                    combined_logs.extend(recent_lines)
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Error reading file {file_path}: {str(e)}"
                }

        # Write combined logs to output file
        full_output_path = os.path.join("..", output_file_path)
        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)
        
        with open(full_output_path, 'w') as f:
            f.writelines(combined_logs)

        return {
            "status": "success",
            "message": f"Successfully wrote {len(combined_logs)} lines from {len(selected_files)} files to {output_file_path}",
            "files_processed": len(selected_files),
            "total_lines": len(combined_logs)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing request: {str(e)}"
        }