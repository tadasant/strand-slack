from app.factory.BotThread import BotThread
from app import app


class BotMonitor:
    def __init__(self):
        self.bot_threads = []

    def create_bot(self, name):
        bot_thread = BotThread(name)
        bot_thread.start()

        app.logger.info(f'New bot started: {bot_thread.name}')

        self.bot_threads.append(bot_thread)

    def count_bots(self):
        app.logger.info(f'{len(self.bot_threads)} bots running!')
        return len(self.bot_threads)

    def list_bots(self):
        for bot_thread in self.bot_threads:
            yield {'bot': bot_thread.bot_name, 'is_alive': bot_thread.is_alive()}

    def start_bots(self):
        app.logger.info(f'Starting {len(self.bot_threads)} bots!')

        for bot_thread in self.bot_threads:
            if bot_thread.is_stopped:
                bot_thread.start()

    def stop_bots(self):
        app.logger.info(f'Stopping {len(self.bot_threads)} bots!')

        for bot_thread in self.bot_threads:
            bot_thread.stop()

    def kill_bots(self):
        app.logger.info(f'Killing {len(self.bot_threads)} bots!')

        for idx, bot_thread in enumerate(self.bot_threads):
            if bot_thread.is_stopped:
                bot_thread.join()
            else:
                bot_thread.stop()
                bot_thread.join()
            self.bot_threads.pop(idx)
