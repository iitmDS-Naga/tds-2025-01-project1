import subprocess
import os

async def run_prettier_format(file_path, command_to_run, is_prettier, prettier_version):
    """
    Format the contents of the specified file using prettier.

    Parameters:
    - file_path (str): Path of the file to be formatted.
    - command_to_run (str): Command used for running prettier.
    - is_prettier (str): Check if the command uses prettier.
    - prettier_version (str): Version of prettier being used.

    Returns:
    - dict: A dictionary with the status and message of the operation.
    """
    if is_prettier.lower() == 'true':
        try:
            if not os.path.exists(file_path):
                return {
                    "status": "error",
                    "message": f"File not found at path: {file_path}"
                }
            full_command = f"npx {command_to_run} --write {file_path}"
            result = subprocess.run(full_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return {
                "status": "success",
                "message": f"File {file_path} formatted successfully using prettier@{prettier_version}.",
                "output": result.stdout.decode()
            }
        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "message": f"Error formatting file {file_path} using prettier@{prettier_version}.",
                "output": e.stderr.decode()
            }
    else:
        return {
            "status": "error",
            "message": "The command does not use prettier."
        }

# Example usage
# result = run_prettier_format("/data/format.md", "prettier", "true", "3.4.2")
# print(result)