import sys
from pathlib import Path
import logging

logger = logging.getLogger()
def add_logging_handlers(filename = 'rmcalyse.log'):
    path = Path(filename).expanduser().absolute()
    f_handler = logging.FileHandler(path, mode='w')
    f_handler.setLevel(logging.DEBUG)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(f_handler)
    logger.info('log file handler added')
    s_handler = logging.StreamHandler(sys.stdout)
    s_handler.setLevel(logging.INFO)
    s_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    s_handler.setFormatter(s_format)
    logger.addHandler(s_handler)
    
add_logging_handlers()
