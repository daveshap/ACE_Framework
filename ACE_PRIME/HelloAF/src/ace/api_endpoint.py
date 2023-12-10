import os
import threading
import json

from http.server import HTTPServer, BaseHTTPRequestHandler

from ace.logger import Logger
from ace import constants

logger = Logger(os.path.basename(__file__))


class StatusHandler(BaseHTTPRequestHandler):
    CALLBACKS = {}

    @classmethod
    def set_callbacks(cls, callbacks):
        cls.CALLBACKS = callbacks

    def __init__(self, *args, **kwargs):
        self.ROUTES = {
            "/status": self.CALLBACKS.get("status", self._handle_default),
        }
        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            handler = self.ROUTES.get(self.path)
            if handler:
                data = handler()
                self._handle_callback_response(data)
            else:
                self._handle_default()

        except Exception as e:
            logger.exception(f"Error handling request: {e}")
            self.respond(500, {"error": "Internal server error"})

    def _handle_callback_response(self, data):
        self.respond(200, data)

    def _handle_default(self):
        self.respond(404, {"error": "Path not found"})

    def respond(self, status_code, content):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(content).encode())

    def log_message(self, format, *args):
        logger.debug(format, *args)


class ApiEndpoint:
    def __init__(
        self, callbacks, api_endpoint_port=constants.DEFAULT_API_ENDPOINT_PORT
    ):
        self.callbacks = callbacks
        self.api_endpoint_port = api_endpoint_port
        self.server = None

    def start_endpoint(self):
        logger.info("Starting API endpoint...")
        StatusHandler.set_callbacks(self.callbacks)
        self.server = HTTPServer(("localhost", self.api_endpoint_port), StatusHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        logger.info("API endpoint started")

    def stop_endpoint(self):
        if self.server:
            logger.info("Shutting down API endpoint...")
            self.server.shutdown()
            self.thread.join()
            logger.info("API endpoint shut down")
