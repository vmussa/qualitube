import logging
import sys

logger = logging.getLogger('qualitube')
logger.setLevel('INFO')
logger.addHandler(logging.FileHandler('pipeline.log'))
logger.addHandler(logging.StreamHandler(sys.stdout))
