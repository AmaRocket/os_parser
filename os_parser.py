import logging
import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

endpoint = (r"/home/xcloud/PycharmProjects/parser/")  # Endpoint foe parsing
# endpoint = "/var/spool/asterisk/asternic/"


class Handler(PatternMatchingEventHandler):

    def on_created(self, event):
        path = event.src_path
        event_type = event.event_type
        print(event_type)
        print(path)
        print("=======================================================================================================")

    def on_deleted(self, event):
        path = event.src_path
        event_type = event.event_type
        print(event_type)
        print(path)
        print("=======================================================================================================")

    def on_moved(self, event):
        path = event.src_path
        event_type = event.event_type
        print(event_type)
        print(path)
        print("=======================================================================================================")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    path = Path(endpoint).resolve().parent

    event_handler = Handler(
        patterns=["*.mp3"]  # Parse files by format
    )

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
