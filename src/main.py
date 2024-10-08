"""This module main cycle in AI assistant jarvis"""
import logging
import os
from typing import Any, Dict, List, Tuple, Union, Optional, Callable
import json
from wake_word import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='jarvis.log', filemode='w', encoding='utf-8')


def load_data_config(settings_file: Optional[str] = None) -> Dict[str, Any]:
    """This function is load data from config file
    :return Dict[str, Any]: Dict of data from config file
    :exception FileNotFound: If there is no config file
    """
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError as e:
        logging.error("config file not found. Path: %s", settings_file)
        raise e


def save_data_config(data: Dict[str, Any], settings_file: Optional[str] = None) -> None:
    """This function is safe data to config file
    :param data: Dict[str, Any]
    :param settings_file: Optional[str]
    """
    logging.info("Saving config file: %s", settings_file)
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info("Config file saved")


def wake_word_detection_handler(module_wake_word: Optional[WakeWord]) -> bool:
    """This function is wake word detection handler
    :type module_wake_word: WakeWord
    """
    logging.info("wake word detected start work ")
    if module_wake_word is None:
        logging.error("wake word not found")
        raise AttributeError
    try:
        if module_wake_word.detected():  # call method class wake word
            logging.debug("wake word detected")
            return True
        else:
            logging.debug('wake word not detected')
            return False
    except AttributeError:
        logging.error("wake word not found")
        raise AttributeError


def jarvis_cycle():
    """This function is main cycle in AI assistant jarvis"""
    logging.info("Jarvis cycle start work")
    if not os.path.isdir("data"):
        os.mkdir("data")

    # need to do auto loaded data from config file

    settings_file = r'data/settings.json'
    load_data_config(settings_file=settings_file)

    logging.info("Jarvis data work")

    wake_words: Optional[WakeWord] = None
    tts: Optional[object] = None
    stt: Optional[object] = None

    data = load_data_config(settings_file=settings_file)
    wake_word_module = data['wake_word']
    token_wake_word = data[wake_word_module] if data[wake_word_module] != '' else " "
    match wake_word_module:
        case 'None':
            raise AttributeError
        case "Picovoice":
            wake_words: Optional[WakeWord] = WakeWordPicovoice(token=token_wake_word)

    logging.info("Jarvis end the work")

    while True:
        if wake_word_detection_handler(module_wake_word=wake_words):
            break  #
        else:
            pass


jarvis_cycle()
