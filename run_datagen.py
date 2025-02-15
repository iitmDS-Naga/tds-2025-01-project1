import subprocess
import os


DATA_DIR = '/data'

async def install_uv():
    try:
        # Check if uv is installed
        subprocess.run(['uv', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("uv is already installed")
    except FileNotFoundError:
        print("Installing uv...")
        # Install uv using curl command
        os.system('curl -LsSf https://astral.sh/uv/install.sh | sh')

async def run_datagen(command_to_run=None, file_url=None, argument_to_pass=None, is_url_remote=None, is_remote_safe=None):
    # Install uv
    await install_uv()

    # Ensure uv installation completed successfully
    try:
        subprocess.run(['uv', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return {
            "status": "error",
            "message": "Failed to install uv"
        }

    if not is_remote_safe and is_url_remote:
        return {
            "status": "error",
            "message": "Error: URL is not from the approved source"
        }

    # Download the script
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        # Download the script
        result = subprocess.run(['curl', '-o', f"{DATA_DIR}/datagen.py", file_url], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"Successfully downloaded script from {file_url}")
        else:
            return {
                "status": "error",
                "message": f"Failed to download script from {file_url}"
            }
        
        # Run the script with argument
        process = subprocess.run(['uv', 'run', f"{DATA_DIR}/datagen.py", argument_to_pass], capture_output=True, text=True)
        if process.returncode == 0:
            print(f"Successfully ran datagen.py with argument: {argument_to_pass}")
            return {
                "status": "success",
                "message": f"Successfully ran datagen.py with argument: {argument_to_pass}",
                "output": process.stdout
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to run datagen.py: {process.stderr}"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }
    finally:
        # Clean up downloaded script
        os.remove(f"{DATA_DIR}/datagen.py")