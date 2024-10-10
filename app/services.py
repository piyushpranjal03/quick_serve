import os

from flask import send_file, current_app
from werkzeug.security import safe_join


def serve_file(file_path):
    base_dir = current_app.config['FILES_DIRECTORY']

    current_app.logger.info(f"Attempting to serve file: {file_path}")

    try:
        full_path = safe_join(base_dir, file_path)
    except ValueError:
        # safe_join will raise a ValueError if the resulting path would fall outside of base_dir
        raise FileNotFoundError(f"Invalid file path: {file_path}")

    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    current_app.logger.info(f"Serving file: {file_path}")
    return send_file(full_path)


def list_files():
    base_dir = current_app.config['DIRECTORY']
    file_list = []

    for root, directories, files in os.walk(str(base_dir)):
        # Add directories
        for directory in directories:
            full_path = os.path.join(root, directory)
            rel_path = os.path.relpath(str(full_path), str(base_dir))
            file_list.append(rel_path + '/')  # Add trailing slash to indicate directory

        # Add files
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(str(full_path), str(base_dir))
            file_list.append(rel_path)

    return file_list
