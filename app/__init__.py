from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.logger import get_logger


webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.logger = get_logger('webserver_logger', 'webserver.log')

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

from app import routes
