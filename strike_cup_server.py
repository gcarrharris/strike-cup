"""Strike Cup local server.

Serves strike-cup.html and forwards three read-only, public Strike endpoints
so the page can show live trader data:

  /api/filters          -> GET /v2/copy/discover/filters
  /api/discover?...     -> GET /v2/copy/discover?...   (all filters passed through)
  /api/trader/<addr>    -> GET /v2/copy/discover/<addr>

No API key is needed. Python 3.8+ standard library only.

Run:  python strike_cup_server.py
Then open http://localhost:8000
"""
import json
import os
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STRIKE = os.environ.get("STRIKE_API", "https://api.strikefinance.org")
PORT = int(os.environ.get("PORT", "8000"))
HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "strike-cup.html")
CACHE_SECONDS = 30
_cache = {}


def strike_get(path):
    hit = _cache.get(path)
    if hit and time.time() - hit[0] < CACHE_SECONDS:
        return hit[1]
    req = urllib.request.Request(
        STRIKE + path,
        headers={"Accept": "application/json", "User-Agent": "strike-cup/0.2"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        body = r.read()
    _cache[path] = (time.time(), body)
    return body


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urllib.parse.urlsplit(self.path)
        try:
            if url.path in ("/", "/index.html"):
                with open(PAGE, "rb") as f:
                    return self._send(200, f.read(), "text/html; charset=utf-8")
            if url.path == "/api/filters":
                return self._send(200, strike_get("/v2/copy/discover/filters"))
            if url.path == "/api/discover":
                qs = ("?" + url.query) if url.query else ""
                return self._send(200, strike_get("/v2/copy/discover" + qs))
            if url.path.startswith("/api/trader/"):
                addr = urllib.parse.quote(url.path.rsplit("/", 1)[-1])
                return self._send(200, strike_get("/v2/copy/discover/" + addr))
            return self._send(404, b'{"error":"not found"}')
        except urllib.error.HTTPError as e:
            return self._send(e.code, e.read() or json.dumps({"error": str(e)}).encode())
        except Exception as e:  # network down, timeout, etc.
            return self._send(502, json.dumps({"error": str(e)}).encode())

    def log_message(self, fmt, *args):
        print("%s  %s" % (self.command, self.path))


if __name__ == "__main__":
    print(f"Strike Cup running at http://localhost:{PORT}  (Strike API: {STRIKE})")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
