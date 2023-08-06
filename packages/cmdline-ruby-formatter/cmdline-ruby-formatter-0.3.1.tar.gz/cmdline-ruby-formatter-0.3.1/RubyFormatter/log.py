import logging

"""
Make notes by logging
"""

logger = logging.getLogger('Formatter')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)2s() - %(message)s')

file_handler = logging.FileHandler(filename='./ruby_file_formatter.log', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
