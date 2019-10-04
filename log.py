import logging
import os

def create_logger(level=logging.INFO):
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=level,
        format='%(levelname)s [%(asctime)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(filename=os.path.join('logs', 'logger.log'), mode='w'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()
