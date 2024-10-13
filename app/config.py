import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))  # Current directory (app)
    PROJECT_ROOT = os.path.dirname(CURRENT_DIR)  # Project root directory (one level up from CURRENT_DIR)

    PORT = int(os.environ.get('PORT', 8081))
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1')

    # Files directory setup
    FILES_DIRECTORY = os.environ.get('FILES_DIRECTORY')
    if not FILES_DIRECTORY:
        FILES_DIRECTORY = 'files' if FLASK_ENV == 'development' else os.path.join('app', 'files')
    FILES_DIRECTORY = os.path.join(PROJECT_ROOT, FILES_DIRECTORY)

    # Logs directory setup
    LOG_BASE = os.environ.get('LOG_BASE')
    if not LOG_BASE:
        LOG_BASE = 'logs' if FLASK_ENV == 'development' else os.path.join('app', 'logs')
    LOG_DIRECTORY = os.path.join(PROJECT_ROOT, LOG_BASE) #Removed environment specific nesting


    # Creating directories if they don't exist
    for directory in [FILES_DIRECTORY, LOG_DIRECTORY]:
        os.makedirs(directory, exist_ok=True)
