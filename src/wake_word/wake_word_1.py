import logging
from abc import ABC, abstractmethod
import pvporcupine
from pvrecorder import PvRecorder
import os
import json


class WakeWord(ABC):
    @abstractmethod
    def __init__(self, token: str) -> None:
        pass

    @abstractmethod
    def detected(self) -> int:
        pass


class WakeWordPicovoice(WakeWord):

    @staticmethod
    def save_token(token: str) -> None:
        logging.info("Loading token from settings.json")
        with open(r"data/settings.json", "r") as f:
            data = json.load(f)
            logging.debug("Token from settings.json: {}".format(data["Picovoice"]))
            data["Picovoice"] = token
        logging.debug("Saving token to settings.json")
        with open(r"data/settings.json", "w") as f:
            json.dump(data, f)
        logging.info("Token saved to settings.json")

    def __init__(self, token: str) -> None:
        """
        :rtype: None
        """
        self.token = token

    def detected(self) -> int:
        try:
            porcupine = pvporcupine.create(access_key=self.token, keywords=["jarvis"])
            recoder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

            try:
                recoder.start()

                while True:
                    keyword_index = porcupine.process(recoder.read())
                    if keyword_index >= 0:
                        print(f"Detected Jarvis")
                        return True

            except KeyboardInterrupt as e:
                """Emergency program shutdown"""
                logging.error(f"Error detected: {e}")
                recoder.stop()
                return False
            finally:
                """clear members"""
                porcupine.delete()
                recoder.delete()
        except pvporcupine._porcupine.PorcupineInvalidArgumentError as e:
            """Error with picovoice module or incorrect token picovoice"""
            print(f"Error: {e}")
            print("Please check your token")
            logging.warning(f"Error: {e}")
            self.token = input("Enter new token: ")
            self.save_token(self.token)
            return False
