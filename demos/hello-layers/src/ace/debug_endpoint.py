import os
import threading
import json

from http.server import HTTPServer, BaseHTTPRequestHandler

from ace.logger import Logger
from ace import constants

logger = Logger(os.path.basename(__file__))


class StatusHandler(BaseHTTPRequestHandler):
    ROUTES = {}

    @classmethod
    def set_routes(cls, routes):
        cls.ROUTES = routes

    def __init__(self, *args, **kwargs):
        self.get_routes = self.ROUTES.get('get', {})
        self.post_routes = self.ROUTES.get('post', {})
        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            handler = self.get_routes.get(self.path, self._handle_default)
            data = handler()
            self._handle_callback_response(data)
        except Exception as e:
            logger.exception(f"Error handling request: {e}")
            self.respond(500, {"error": "Internal server error"})

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data)
            handler = self.post_routes.get(self.path)
            if handler:
                data = handler(post_data)
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
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(content).encode())

    def log_message(self, format, *args):
        logger.debug(format, *args)


class DebugEndpoint:
    def __init__(self, routes, debug_endpoint_port=constants.DEFAULT_DEBUG_ENDPOINT_PORT):
        self.routes = routes
        self.debug_endpoint_port = debug_endpoint_port
        self.server = None

    def start_endpoint(self):
        logger.info("Starting debug endpoint...")
        StatusHandler.set_routes(self.routes)
        self.server = HTTPServer(('localhost', self.debug_endpoint_port), StatusHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        logger.info("Debug endpoint started")

    def stop_endpoint(self):
        if self.server:
            logger.info("Shutting down debug endpoint...")
            self.server.shutdown()
            self.thread.join()
            logger.info("Debug endpoint shut down")
