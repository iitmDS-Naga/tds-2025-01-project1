import pandas as pd
import os

async def run_count_days(input_file_path, weekday_to_count, output_file_path, request_to_count):
    """
    Count the occurrences of a specific weekday in a date column from input file and write result to output file.

    Parameters:
    - input_file_path (str): Path of the input file to read
    - weekday_to_count (str): Name of the weekday to count
    - output_file_path (str): Path of the output file to write results
    - request_to_count (str): Boolean string indicating if counting is requested

    Returns:
    - dict: A dictionary with the status and message of the operation
    """
    # If output path is empty, create a default path based on weekday
    if not output_file_path:
        output_file_path = f"dates-{weekday_to_count.lower()}s.txt"
    
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

        # Read the CSV file
        df = pd.read_csv("../" + input_file_path, names=['date'], header=None, delimiter='\n', on_bad_lines='skip')
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce', infer_datetime_format=True)

                # Check for any NaT values in the 'date' column
        if df['date'].isna().any():
            return {
                "status": "error",
                "message": "Error converting date column to datetime. Please check the date format in the input file."
            }
        
        # Get day name and count occurrences of specified weekday
        weekday_counts = df[df['date'].dt.day_name() == weekday_to_count.capitalize()].shape[0]
        
        # Create result string
        result = f"Number of {weekday_to_count}s: {weekday_counts}\n"
        
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

# Example usage
# result = await run_count_days("input.csv", "Monday", "output.txt", "true")
# print(result)