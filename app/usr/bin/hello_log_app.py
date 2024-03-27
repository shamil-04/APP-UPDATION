import configparser
import logging
import threading
import time
import os

BASE=os.path.expanduser('~')+"/projects/app/"

CONFIG=BASE+'config/config.ini'
LOG=BASE+'log/log.txt'

def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG)
    return config.get('MESSAGE', 'greeting')

def log_message(greeting):
    logging.basicConfig(filename=LOG, level=logging.INFO, format='%(asctime)s - %(message)s')
    logging.info(f"{greeting} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    threading.Timer(5.0, log_message, args=(greeting,)).start()

def main():
    greeting = read_config()
    log_message(greeting)

if __name__ == "__main__":
    main()
