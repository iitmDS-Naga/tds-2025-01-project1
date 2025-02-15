import pandas as pd
import os
from datetime import datetime
import dateparser

async def run_count_days(input_file_path, weekday_to_count, request_to_count, output_file_path = None):
    """
    [... existing docstring ...]
    """
    # If output path is empty, create a default path based on weekday
    if not output_file_path:
        output_file_path = f"data/dates-{weekday_to_count.lower()}s.txt"
    
    if request_to_count.lower() != 'true':
        return {
            "status": "error",
            "message": "Not a valid count request"
        }

    try:
        # Check if input file exists
        if not os.path.exists("../" + input_file_path):
            return {
                "status": "error",
                "message": f"Input file not found at: {input_file_path}"
            }

        # Read the txt file and process dates
        with open("../" + input_file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        
        # Use dateparser for flexible date parsing
        parsed_dates = []
        for date_str in lines:
            try:
                parsed_date = dateparser.parse(date_str)
                if parsed_date:
                    parsed_dates.append(parsed_date)
                else:
                    return {
                        "status": "error",
                        "message": f"Could not parse date: {date_str}"
                    }
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Error parsing date {date_str}: {str(e)}"
                }
        
        # Create DataFrame with parsed dates
        df = pd.DataFrame(parsed_dates, columns=['date'])
        
        # Get day name and count occurrences of specified weekday
        weekday_counts = df[df['date'].dt.day_name() == weekday_to_count.capitalize()].shape[0]
        
        # Create result string
        result = f"{weekday_counts}\n"
        
        # Write to output file
        with open("../" + output_file_path, 'w') as f:
            f.write(result)
            
        return {
            "status": "success",
            "message": f"Successfully counted {weekday_to_count}s and wrote result to {output_file_path}",
            "count": weekday_counts
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing request: {str(e)}"
        }