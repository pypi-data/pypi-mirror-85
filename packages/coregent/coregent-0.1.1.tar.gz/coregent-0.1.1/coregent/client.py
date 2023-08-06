import argparse
import socket
import _thread

from .networking import get_client_socket, JSONReader, JSONWriter


class Client:
    def __init__(self, hostname, port, on_message):
        self.hostname = hostname
        self.port = port
        self.on_message = on_message
        self.writer = None

    def start(self):
        """
        Kick off the client mainloop, connecting to the configured server and
        initiating the message reader event handler.
        """
        # Utilize functionality to autodetect the socket configuration needed.
        connection = get_client_socket(self.hostname, self.port)

        # We need a reference to the writer to send it messages.
        self.writer = JSONWriter(connection)
        # The reader is expected to be utilized only through the registered
        # callback.
        reader = JSONReader(connection)

        # Start the reader mainloop to avoid blocking this method's caller.
        _thread.start_new_thread(self.handle_messages, (reader,))

    def handle_messages(self, reader):
        """
        Mainloop for processing incoming messages.
        """
        for message in reader:
            self.on_message(message)

        reader.close()

    def send_message(self, message):
        """
        Send @message, a JSON-encodable object, to the server.
        """
        self.writer.send(message)

    def close(self):
        """
        Cleanly shut down the connection to the server.
        """
        self.writer.close()


class ConsoleClient(Client):
    """
    An example CLI Client, capable of sending and receiving simple chat
    messages and logging raw messages of other types.
    """

    def __init__(self, hostname, port):
        super().__init__(hostname, port, self.display_message)

    def display_message(self, message):
        """
        Display a single Python dictionary pre-decoded from JSON.
        """
        if message['type'] != 'chat':
            print(f'Unknown message: {message}')

        if message['source'] == 'server':
            print(f'!! {message["msg"]}')
        else:
            print(f'{message["user"]}: {message["msg"]}')

    def run(self):
        """
        Connect to the configured server and run the interactive mainloop.
        """
        self.start()

        while True:
            message = input(' -> ')
            if message.lower().startswith('bye'):
                self.close()
                break

            self.send_message({
                'type': 'chat',
                'msg': message
            })


class ConnectionManager:
    """
    Create and manage labeled connections.
    """

    def __init__(self):
        self.connections = {}
        self.listeners = {}

    def open_connection(self, name, hostname, port, on_message=None):
        """
        Open a TCP connection to the specified @hostname and @port, storing it
        as @name. If a connection with the specified @name already exists, it
        will be closed. If @on_message is specified, it will be passed to
        `register_listener()`. In all cases, any existing listeners will be
        retained.
        """
        # We don't forcibly clear listeners so that this method can be used to
        # revive a connection. Not perfect so this bears revisiting.
        self.listeners.setdefault(name, [])
        if on_message:
            self.register_listener(name, on_message)

        # We want to support registering multiple listeners for a single
        # connection, so we defer resolution of the callbacks to the last
        # moment.
        new_conn = Client(hostname, port, lambda m: self._handle_message(name, m))
        # Start the client mainloop.
        new_conn.start()

        # Detect and dispose of any previously existing connection.
        old_conn = self.connections.get(name)
        if old_conn:
            old_conn.close()

        # Now that the new connection has been established, mark it as usable.
        self.connections[name] = new_conn



    def close_connection(self, name):
        """
        Close the connection with the specified @name. Does not discard any
        existing listeners.
        """
        self.connections.pop(name).close()

    def register_listener(self, name, on_message):
        """
        Register @on_message as a callback for messages received from the
        connection specified as @name. @on_message should accept one argument:
        a parsed JSON message.
        """
        self.listeners[name].append(on_message)

    def send_message(self, name, message):
        """
        Send @message, a JSON-encodable object, to the connection specified as
        @name.
        """
        return self.connections[name].send_message(message)

    def _handle_message(self, name, message):
        for listener in self.listeners[name]:
            listener(message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--hostname', default='localhost')
    parser.add_argument('-p', '--port', type=int, default=40001)
    args = parser.parse_args()

    ConsoleClient(args.hostname, args.port).run()
