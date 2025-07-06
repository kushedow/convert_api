import os
import subprocess
import base64
import uuid

def convert_docx_file_to_pdf(source_path):

    command = [
        "soffice",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        "./temp",
        source_path
    ]

    try:

        result = subprocess.run(command, capture_output=True, text=True, check=True)

        if result.returncode != 0:
            print(f"STDOUT: {source_path}", result.stdout)
        else:
            print(f"STDERR: {source_path}", result.stderr)
        print("Command executed")

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Return code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
    except FileNotFoundError:
        print("Error: 'soffice' command not found. Make sure LibreOffice is installed and in your PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output
