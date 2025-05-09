import json
import os

def read_json_file(file_path):
    """
    Reads a JSON file and returns its content.
    
    Args:
        file_path (str): The path to the JSON file.
        
    Returns:
        dict: The content of the JSON file.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    absolute_path = os.path.join(base_dir, file_path)

    with open(absolute_path, 'r', encoding="utf8") as file:
        return json.load(file)