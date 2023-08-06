import json
import socket

import ijson


def get_socket_type(host=None, ip_type=None):
    if ip_type is not None:
        return ip_type

    if host and ':' in host:
        return socket.AF_INET6

    return socket.AF_INET


def get_server_socket(host, port, ip_type=None):
    sock = socket.socket(get_socket_type(host, ip_type))
    sock.bind((host, port))
    return sock

def get_client_socket(host, port, ip_type=None):
    sock = socket.socket(get_socket_type(host, ip_type))
    sock.connect((host, port))
    return sock


class _SocketFile:
    def __init__(self, sock):
        self.sock = sock

    def read(self, chunk=4096):
        return self.sock.recv(chunk).decode()


class JSONReader:
    def __init__(self, sock):
        self.sock = sock
        self.processor = ijson.items(_SocketFile(sock), 'item')

    def __next__(self):
        return next(self.processor)

    def __iter__(self):
        yield from self.processor

    def close(self):
        self.sock.close()


class JSONWriter:
    def __init__(self, sock):
        self.sock = sock
        self.prefix = b'['

    def send(self, message):
        self.sock.sendall(self.prefix + json.dumps(message).encode())
        self.prefix = b','


    def close(self):
        self.sock.sendall(b']')
        self.sock.close()
