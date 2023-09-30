from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class StatusHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.ROUTES = {
            '/status': self._handle_status,
            # Add more paths here...
        }
        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            handler = self.ROUTES.get(self.path, self._handle_default)
            handler()
        except Exception as e:
            logger.exception(f"Error handling request: {e}")
            self.respond(500, {"error": "Internal server error"})

    def _handle_status(self):
        self.respond(200, {"healthy": True})

    def _handle_default(self):
        self.respond(404, {"error": "Resource not found"})

    def respond(self, status_code, content):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(content).encode())

    def log_message(self, format, *args):
        logger.debug(format, *args)


class ApiEndpoint:
    def __init__(self, api_endpoint_port=3000):
        self.api_endpoint_port = api_endpoint_port
        self.server = None

    def start_endpoint(self):
        logger.info("Starting API endpoint...")
        self.server = HTTPServer(('localhost', self.api_endpoint_port), StatusHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        logger.info("API endpoint started")

    def stop_endpoint(self):
        if self.server:
            logger.info("Shutting down API endpoint...")
            self.server.shutdown()
            self.thread.join()
            logger.info("API endpoint shut down")
