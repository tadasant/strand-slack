import threading
import time


class BotThread(threading.Thread):
    def __init__(self):
        super(BotThread, self).__init__()
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self.daemon = True

    @property
    def is_paused(self):
        return self._pause_event.is_set()

    @property
    def is_stopped(self):
        return self._stop_event.is_set()

    def pause(self):
        self._pause_event.set()

    def resume(self):
        self._pause_event.clear()

    def run(self):
        self._stop_event.clear()
        while not self._stop_event.is_set():
            while not self._pause_event.is_set():
                time.sleep(1)
                print(self.name)

    def stop(self):
        self._stop_event.set()
