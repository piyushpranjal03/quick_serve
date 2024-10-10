from flask import Blueprint, abort, current_app

from app.services import serve_file, list_files

main = Blueprint('main', __name__)


@main.route('/files/<path:filepath>')
def file_route(filepath):
    try:
        return serve_file(filepath)
    except FileNotFoundError as e:
        current_app.logger.warning(f"File not found: {filepath}. Error: {str(e)}")
        abort(404, description=str(e))
    except Exception as e:
        current_app.logger.error(f"Error serving file {filepath}: {str(e)}")
        abort(500, description="Error serving file")


@main.route('/list')
def list_route():
    try:
        files = list_files()
        current_app.logger.info(f"Listed {len(files)} files")
        return {"files": files}
    except Exception as e:
        current_app.logger.error(f"Error listing files: {str(e)}")
        abort(500, description="Error listing files")


@main.route('/health')
def health_check():
    current_app.logger.info("Health check performed")
    return {"status": "healthy"}, 200
