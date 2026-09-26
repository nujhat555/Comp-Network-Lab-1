# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverSocket.bind(("", port))
    serverSocket.listen(1)

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()

        try:
            message = connectionSocket.recv(4096).decode("iso-8859-1")
            request_line = message.splitlines()[0] if message else ""
            request_parts = request_line.split()
            if len(request_parts) < 2:
                raise FileNotFoundError

            # Get the requested path, excluding the query string.
            filename = request_parts[1].split("?", 1)[0]
            if filename == "/":
                filename = "/index.html"
            filename = filename.lstrip("/")

            # Open the client-requested file as bytes for socket transmission.
            with open(filename, "rb") as f:
                file_contents = f.read()

            # Prepare the headers for a successful response.
            outputdata = b"HTTP/1.1 200 OK\r\n"
            outputdata += b"Server: SimplePythonWebServer\r\n"
            outputdata += b"Content-Type: text/html; charset=UTF-8\r\n"
            outputdata += b"Content-Length: " + str(len(file_contents)).encode("ascii") + b"\r\n"
            outputdata += b"Connection: close\r\n\r\n"
            outputdata += file_contents

            # Send the complete response in one call.
            connectionSocket.send(outputdata)
            connectionSocket.close()

        except Exception:
            # Send a 404 response for a missing file or invalid request.
            body = b"<html><head><title>404 Not Found</title></head>" \
                   b"<body><h1>404 Not Found</h1></body></html>"
            outputdata = b"HTTP/1.1 404 Not Found\r\n"
            outputdata += b"Server: SimplePythonWebServer\r\n"
            outputdata += b"Content-Type: text/html; charset=UTF-8\r\n"
            outputdata += b"Content-Length: " + str(len(body)).encode("ascii") + b"\r\n"
            outputdata += b"Connection: close\r\n\r\n"
            outputdata += body
            try:
                connectionSocket.send(outputdata)
            except Exception:
                pass
            connectionSocket.close()

    # Commenting out the below (some use it for local testing). It is not required for Gradescope, and some students have moved it erroneously in the While loop.
    # DO NOT PLACE ANYWHERE ELSE AND DO NOT UNCOMMENT WHEN SUBMITTING, YOU ARE GONNA HAVE A BAD TIME
    # serverSocket.close()
    # sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)
