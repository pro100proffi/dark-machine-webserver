import socket
import os
import subprocess
import sys
HOST = "127.0.0.1"
PORT = 8080

PUBLIC_DIR = "public"


MIME_TYPES = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif"
}


def get_content_type(path):
    ext = os.path.splitext(path)[1]
    return MIME_TYPES.get(ext, "application/octet-stream")


def build_response(status_code, body=b"", content_type="text/html"):

    status_messages = {
        200: "OK",
        404: "Not Found"
    }

    status_message = status_messages.get(status_code, "OK")

    headers = [
        f"HTTP/1.1 {status_code} {status_message}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body)}",
        "Connection: close",
        "",
        ""
    ]

    header_bytes = "\r\n".join(headers).encode()

    return header_bytes + body


def run_cgi(script_path):
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    output = result.stdout
    errors = result.stderr

    if errors:
        print("CGI ERRORS:")
        print(errors)

        error_html = f"""
        <h1>CGI script error</h1>
        <pre>{errors}</pre>
        """

        return build_response(
            500,
            error_html.encode("utf-8"),
            "text/html; charset=utf-8"
        )

    if not output.strip():
        empty_html = """
        <h1>CGI returned empty response</h1>
        <p>Скрипт запустился, но ничего не вывел через print().</p>
        """

        return build_response(
            500,
            empty_html.encode("utf-8"),
            "text/html; charset=utf-8"
        )

    return build_response(
        200,
        output.encode("utf-8"),
        "text/html; charset=utf-8"
    )

def handle_request(request_text):

    if not request_text.strip():
        return b""

    lines = request_text.split("\r\n")
    request_line = lines[0]

    if not request_line:
        return b""

    parts = request_line.split()

    if len(parts) < 3:
        return b""

    method, path, version = parts

    print("REQUEST PATH:", path)

    if path.startswith("/cgi-bin/"):
        script_path = path.lstrip("/")

        print("CGI SCRIPT PATH:", script_path)

        if os.path.exists(script_path) and os.path.isfile(script_path):
            return run_cgi(script_path)

        return build_response(
            404,
            b"<h1>CGI script not found</h1>",
            "text/html; charset=utf-8"
        )

    if path == "/":
        path = "/index.html"

    file_path = os.path.join(PUBLIC_DIR, path.lstrip("/"))

    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "rb") as f:
            body = f.read()

        content_type = get_content_type(file_path)

        return build_response(200, body, content_type)

    return build_response(
        404,
        b"<h1>404 Not Found</h1>",
        "text/html; charset=utf-8"
    )


def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST, PORT))

    server_socket.listen(5)

    print(f"Server running on http://{HOST}:{PORT}")

    while True:

        client_socket, address = server_socket.accept()

        request = client_socket.recv(4096)

        request_text = request.decode("utf-8", errors="ignore")

        response = handle_request(request_text)

        client_socket.sendall(response)

        client_socket.close()


if __name__ == "__main__":
    start_server()