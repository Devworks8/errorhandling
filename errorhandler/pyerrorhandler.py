"""
Application Name: Error Handler
File Name: __main__.py
Description: Catch and report all relevant exceptions related to the UPnPHub projects.
"""
__VERSION__ = "0.0.1"

# from time import sleep
import zmq

import errorhandler


class ErrorListerner:
    def __init__(self, url="tcp://*", port=5599, id=b''):
        self.url = url
        self.port = port
        self.state = 0
        self.id = id
        self.reporters = [] # list of tuples of registered reporters

    def initialize(self):
        # TODO: initialize the server and run the state loop
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("{url}:{port}".format(url=self.url, port=self.port))

        print('Binding ErrorHandler to port {port}'.format(port=self.port))
        while True:
            if self.state is errorhandler.STATES['RUNNING']:
                message = socket.recv_multipart()
                if message[0] not in self.reporters and message[1] == b'PING':
                    self.reporters.append(message[0])
                    socket.send_multipart((self.id, b'PONG', b''))
                elif message[0] in self.reporters and message[1] in errorhandler.COMMAND:
                    if message[1] is b'HEART':
                        socket.send_multipart((self.id, b'BEAT', b''))
                    elif message[1] is b'INFO':
                        pass  # Parse Info
                    elif message[1] is b'WARN':
                        pass  # Parse Warnings
                    elif message[1] is b'ERROR':
                        pass  # Parse Errors

    def changestate(self, state):
        if state < 3:
            self.state = state


class ErrorReporter:
    def __init__(self, url="tcp://*", port=5599, id=b''):
        self.url = url
        self.port = port
        self.state = 0
        self.id = id

    def initialize(self):
        # TODO: initialize the server and the state loop
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.bind("{url}:{port}".format(url=self.url, port=self.port))

    def changestate(self, state):
        if state < 3:
            self.state = state

