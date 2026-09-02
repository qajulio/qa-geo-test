#!/usr/bin/env python3
"""Servidor HTTP local single-threaded para servir o relatorio QA-GEO (HTML/MD/TXT).

Uso:
  python serve_report.py --directory ./out --port 8080

Apenas stdlib Python 3.8+. NAO expor para a internet (uso local).
"""
import argparse
import sys
import socket
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def end_headers(self):
        # Headers para seguranca local
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def log_message(self, fmt, *args):
        # Log compacto
        sys.stderr.write(f"[serve] {self.address_string()} - {fmt % args}\n")


def is_port_free(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        try:
            s.connect((host, port))
            return False
        except (ConnectionRefusedError, socket.timeout, OSError):
            return True


def main():
    ap = argparse.ArgumentParser(description="Servidor HTTP local para relatorio QA-GEO")
    ap.add_argument("--directory", required=True, help="Diretorio com os arquivos do relatorio")
    ap.add_argument("--port", type=int, default=8080, help="Porta local (padrao 8080)")
    ap.add_argument("--host", default="127.0.0.1", help="Host (padrao 127.0.0.1 - apenas local)")
    args = ap.parse_args()

    directory = str(Path(args.directory).resolve())
    if not Path(directory).exists():
        sys.exit(f"Erro: diretorio nao encontrado: {directory}")

    if not is_port_free(args.host, args.port):
        sys.exit(f"Erro: porta {args.port} ja esta em uso em {args.host}")

    httpd = HTTPServer((args.host, args.port), lambda *a, **kw: Handler(*a, directory=directory, **kw))
    print(f"[serve] Servindo '{directory}' em http://{args.host}:{args.port}/")
    print(f"[serve] Abra:  http://{args.host}:{args.port}/relatorio.html")
    print(f"[serve] Outros arquivos disponiveis no mesmo diretorio:")
    for f in sorted(Path(directory).iterdir()):
        if f.is_file():
            print(f"         http://{args.host}:{args.port}/{f.name}")
    print(f"[serve] Pressione Ctrl+C para parar.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[serve] Parando servidor...")
        httpd.server_close()


if __name__ == "__main__":
    main()
