"""Development-only static server. Loopback by default; explicit --lan opts into LAN exposure."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        allowed = {'/', '/index.html', '/Lumen-Commons-Play.html', '/src/core.js', '/src/world.js', '/src/game.js', '/src/style.css'}
        if unquote(urlsplit(self.path).path) not in allowed:
            self.send_error(404, 'Not a game asset')
            return None
        return super().send_head()
    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Permissions-Policy', 'camera=(), microphone=(), geolocation=(), payment=(), usb=()')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('Content-Security-Policy', "frame-ancestors 'none'")
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def list_directory(self, path):
        self.send_error(403, 'Directory listings are disabled')
        return None

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--lan', action='store_true')
    p.add_argument('--port', type=int, default=8080)
    a=p.parse_args()
    if not 1024 <= a.port <= 65535: p.error('Choose a port from 1024 to 65535')
    host='0.0.0.0' if a.lan else '127.0.0.1'
    root=Path(__file__).resolve().parent
    print(f'Open http://127.0.0.1:{a.port}/', flush=True)
    if a.lan:
        print(f'LAN enabled. Phone on trusted Wi-Fi: http://YOUR_COMPUTER_LOCAL_IP:{a.port}/', flush=True)
        print('Do not forward this port. This is NOT a production server.', flush=True)
    try:
        with ThreadingHTTPServer((host,a.port), partial(Handler,directory=str(root))) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopped.')
    except OSError as exc:
        raise SystemExit(f'Could not start server: {exc}. Try another --port.')
