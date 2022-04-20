import logging
import time
from pathlib import Path

import google
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

import google_api

endpoint = r"/home/xcloud/PycharmProjects/parser/"  # Endpoint for parsing


# endpoint = "/var/spool/asterisk/asternic/"


class Handler(PatternMatchingEventHandler):
    def on_created(self, event):
        path = event.src_path
        event_type = event.event_type
        print(event_type)
        print(path)
        try:
            print("Trying...")
            google_api.transcribe_file(path)
        except BaseException.with_traceback():
            time.sleep(5)
            print("Trying again...")
            google_api.transcribe_file(path)
        print(
            "======================================================================================================="
        )

    def on_deleted(self, event):
        path = event.src_path
        event_type = event.event_type
        print(event_type)
        print(path)
        print(
            "======================================================================================================="
        )

    def on_moved(self, event):
        path = event.src_path
        event_type = event.event_type
        print(event_type)
        print(path)
        print(
            "======================================================================================================="
        )


def main():
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        path = Path(endpoint).resolve().parent

        event_handler = Handler(patterns=["*.mp3"])  # Parse files by format

        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()
    except google.api_core.exceptions.ServiceUnavailable:
        time.sleep(10)
        main()


if __name__ == "__main__":
    main()
