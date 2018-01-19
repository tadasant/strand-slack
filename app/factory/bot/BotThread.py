import threading
import time

from app import app


class BotThread(threading.Thread):
    def __init__(self):
        super(BotThread, self).__init__()
        self._stop_event = threading.Event()
        self.daemon = True

    @property
    def is_stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self._stop_event.clear()
        while not self._stop_event.is_set():
            time.sleep(1)
            app.logger.debug(self.name)

    def stop(self):
        self._stop_event.set()
