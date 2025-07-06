import os
import base64
import uuid


def save_base64_as_file(base64_string: str, extension: str) -> str | None:

    output_dir = "./temp"
    os.makedirs(output_dir, exist_ok=True)

    random_filename = f"{uuid.uuid4()}"
    output_file_path = os.path.join(output_dir, f"{random_filename}.{extension}")

    try:

        decoded_content = base64.b64decode(base64_string)

        with open(output_file_path, "wb") as f:
            f.write(decoded_content)

        print(f"Successfully saved DOCX file to: {output_file_path}")
        return random_filename

    except TypeError:
        print("Error: Input Base64 string is not valid or incorrectly formatted.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while saving the file: {e}")
        return None


def get_file_content_as_base64(file_path):
    """
    Reads a file from the given path and returns its content
    encoded in Base64.
    """

    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return None

    if not os.path.isfile(file_path):
        print(f"Error: Path '{file_path}' is not a file.")
        return None

    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
            encoded_content = base64.b64encode(file_content)
            return encoded_content.decode('utf-8')

    except IOError as e:
        print(f"Error reading file '{file_path}': {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
