"""Servidor de desenvolvimento do prototipo: estaticos com gzip (como uma hospedagem real) e Cache-Control no-store
(evita ver versao velha). 127.0.0.1 apenas.   Uso: python3 tools/serve.py [porta]"""
import gzip, http.server, mimetypes, os, pathlib, sys, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
COMPRIMIR = {".html", ".css", ".js", ".svg", ".json", ".txt"}


class H(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def do_GET(self):
        self._servir(True)

    def do_HEAD(self):
        self._servir(False)

    def _servir(self, corpo):
        p = urllib.parse.unquote(urllib.parse.urlparse(self.path).path)
        f = (ROOT / p.lstrip("/")).resolve()
        if ROOT not in f.parents and f != ROOT:
            return self._erro(403)
        if f.is_dir():
            f = f / "index.html"
        if not f.is_file():
            return self._erro(404)
        dados = f.read_bytes()
        tipo = mimetypes.guess_type(str(f))[0] or "application/octet-stream"
        if f.suffix == ".woff2":
            tipo = "font/woff2"
        self.send_response(200)
        self.send_header("Content-Type", tipo + ("; charset=utf-8" if tipo.startswith("text/") or tipo.endswith("javascript") or tipo.endswith("svg+xml") else ""))
        if f.suffix in COMPRIMIR and "gzip" in self.headers.get("Accept-Encoding", ""):
            dados = gzip.compress(dados, 6)
            self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(dados)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if corpo:
            self.wfile.write(dados)

    def _erro(self, c):
        self.send_response(c)
        self.send_header("Content-Length", "0")
        self.end_headers()


class S(http.server.ThreadingHTTPServer):
    request_queue_size = 256
    daemon_threads = True


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8741
    S(("127.0.0.1", port), H).serve_forever()
