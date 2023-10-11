import time
import threading
from datetime import datetime


class Telemetry:
    def __init__(self):
        self.data = []
        self.event_listeners = {}
        self.scheduler = None

    def collect_data(self):
        raise NotImplementedError

    # TODO: Implement this.
    def get_data(self, namespace):
        pass

    # TODO: Implement this.
    def get_namespaces(self):
        pass

    def ingest_data(self, data):
        try:
            timestamped_data = (datetime.now(), data)
            self.data.append(timestamped_data)
            self.log.debug(f"Ingested data: {timestamped_data}")
        except Exception as e:
            self.handle_error(e)

    def retrieve_data(self, criteria):
        try:
            return [d for d in self.data if criteria(d)]
        except Exception as e:
            self.handle_error(e)
            return None

    def export_data(self, format):
        raise NotImplementedError

    def handle_error(self, error):
        self.log.error(f"Error occurred: {str(error)}")

    def schedule_collection(self, interval):
        def job():
            while True:
                self.collect_data()
                time.sleep(interval)
        self.scheduler = threading.Thread(target=job)
        self.scheduler.start()

    def register_event_listener(self, event, callback):
        if event not in self.event_listeners:
            self.event_listeners[event] = []
        self.event_listeners[event].append(callback)

    def check_threshold(self, threshold, value):
        if value > threshold:
            for callback in self.event_listeners.get('threshold_exceeded', []):
                callback(value)

    def start(self):
        if self.scheduler:
            self.scheduler.start()

    def stop(self):
        if self.scheduler:
            self.scheduler.join()

    def reset(self):
        self.data = []
        self.log.debug("Data reset")
