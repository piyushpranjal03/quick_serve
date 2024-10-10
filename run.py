import logging
import os
from logging.handlers import TimedRotatingFileHandler

from app import create_app
from app.config import Config

app = create_app()

# Configure logging
log_file_path = os.path.join(Config.LOG_DIRECTORY, 'log')
file_handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=1, backupCount=10)
file_handler.suffix = '%Y-%m-%d'
file_handler.setFormatter(logging.Formatter('%(asctime)s:::%(filename)s:::%(levelname)s:::%(message)s'))

# Add the file handler to the app logger
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


if __name__ == '__main__':
    app.logger.info(f'Starting application on port {Config.PORT} in {Config.FLASK_ENV} environment')
    app.logger.info(f'Files will be served from: {Config.FILES_DIRECTORY}')
    app.logger.info(f'Logs will be written to: {Config.LOG_DIRECTORY}')

    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
