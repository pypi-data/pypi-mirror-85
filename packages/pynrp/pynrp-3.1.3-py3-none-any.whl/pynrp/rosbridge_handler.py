# ---LICENSE-BEGIN - DO NOT CHANGE OR MOVE THIS HEADER
# This file is part of the Neurorobotics Platform software
# Copyright (C) 2014,2015,2016,2017 Human Brain Project
# https://www.humanbrainproject.eu
#
# The Human Brain Project is a European Commission funded project
# in the frame of the Horizon2020 FET Flagship plan.
# http://ec.europa.eu/programmes/horizon2020/en/h2020-section/fet-flagships
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# ---LICENSE-END
"""
An interface to handle rosbridge communication
"""

import roslibpy
import logging
from multiprocessing import Process, Pipe
from threading import Thread
import time

_CONNECTION_TIMEOUT = 10  # seconds before stop waiting for rosbridge connection


class RosBridgeConnectError(Exception):
    """
    Type of error risen when there are connection issues
    """
    pass


# TODO: add unit tests
class RosBridgeHandler(object):
    """
    Provides a convenient interface to connect to RosBridge and handle properly connection error,
    disconnections, etc
    """

    def __init__(self):
        """
        Creates an instance of this class
        """

        self._logger = logging.getLogger('RosBridgeHandler')
        self._is_init = False
        self._was_closed = False
        self._client = None
        self._topics = {}

    @property
    def is_init(self):
        """
        Returns True if the handler has been initialized
        """
        return self._is_init

    @is_init.setter
    def is_init(self, value):
        """
        Setter method for is_init property

        :param value: boolean value for is_init property
        """
        self._is_init = value

    def initialize(self, host, port=None):
        """
        Initializes the handler if it is not initialized yet and it was not initialized before.
        Creates a RosBridge client and connects it to the server. Raises RosBridgeConnectError
        in case of connection errors.

        :param host: string representing the ip of the RosBridge server
        :param port: (optional) integer corresponding to the RosBridge server port. None by default.
        """
        # Check flags
        if self._is_init:
            self._logger.info('Rosbridge client already initialized')
            return
        elif self._was_closed:
            self._logger.info('Re-initializing a Rosbridge client is not allowed. it is not '
                              'recommended to initialized any other client in the same process. '
                              'Use class RosBridgeHandlerProcess if you need to do that')
            return

        has_failed = False

        # Connect to rosbridge server
        try:
            self._client = roslibpy.Ros(host=host, port=port)
            self._client.run(_CONNECTION_TIMEOUT)
        # pylint: disable=broad-except
        except Exception:
            has_failed = True
        else:
            if not self._client.is_connected:
                has_failed = True

        if has_failed:
            raise RosBridgeConnectError('Rosbridge client could not connect to server')

        self._is_init = True

    def subscribe_topic(self, name, ros_type, callback):
        """
        Subscribes a callback to a Ros topic

        :param name: string corresponding to the topic address
        :param ros_type: string corresponding to the topic type
        :param callback: function object to be called upon new message
        """
        if not self._is_init:
            self._logger.info('Rosbridge client was not correctly initialized. Could not subscribe '
                              'to: %s', name)
            return

        self._topics[name] = roslibpy.Topic(self._client, name, ros_type)
        self._topics[name].subscribe(callback)

    def unsubscribe_topic(self, name):
        """
        Unsubscribes a callback to a Ros topic

        :param name: string corresponding to the topic address
        """
        if name in self._topics:
            self._topics[name].unsubscribe()
        else:
            self._logger.info('RosBridge client was not subscribed to: %s', name)

    def close(self):
        """
        Closes the RosBridge connection. After this the handler can not be initialized again.
        Furthermore, it is not recommended to initialized any other client in the same process.
        Use class RosBridgeHandlerProcess if you need to do that.
        """
        if not self._is_init:
            self._logger.info('Rosbridge client was not correctly initialized. Cannot be closed')
            return

        for name in self._topics:
            self.unsubscribe_topic(name)

        self._client.close()
        self._was_closed = True
        self._is_init = False
        self._logger.info('RosBridge client was closed correctly')


# TODO: add unit tests
class RosBridgeHandlerProcess(RosBridgeHandler):
    """
    Extension of RosBridgeHandler that runs the RosBridge client in a separate process. This is
    convenient when starting more than one client from the same process is required.
    RosBridgeHandler can give problems in this case due to limitations in roslibpy / twisted for
    handling re-connections and multiple connections.
    """

    def __init__(self):
        """
        Creates an instance of this class
        """
        super().__init__()

        self._pipe = None
        self._rb_process = None
        self._rb_proxy = None
        self._in_process = False
        self._callbacks = {}

    def initialize(self, host, port=None):
        """
        Initializes the handler if it is not initialized yet and it was not initialized before.
        Creates a RosBridge client and connects it to the server. Raises RosBridgeConnectError
        in case of connection errors.

        :param host: string representing the ip of the RosBridge server
        :param port: (optional) integer corresponding to the RosBridge server port. None by default.
        """
        if self.is_init:
            self._logger.info('Rosbridge client already initialized')
            return

        self._pipe = Pipe()

        # starts process with rosbridge client
        self._rb_process = Process(target=self._event_loop_process, args=(host, port,))
        self._rb_process.start()

        # starts thread handling callbacks
        self._rb_proxy = Thread(target=self._event_loop_proxy)
        self._rb_proxy.start()

        # waits for initialization is completed
        n = 0
        while not self.is_init and n < _CONNECTION_TIMEOUT:
            n += 1
            time.sleep(1)

        if not self.is_init:
            raise RosBridgeConnectError('Rosbridge client could not connect to server')

    def _event_loop_process(self, host, port=None):
        """
        Method handling the communication with the RosBridge server from a separate process

        :param host: string representing the ip of the RosBridge server
        :param port: (optional) integer corresponding to the RosBridge server port. None by default.
        """
        # everything is executed inside of the forked process from now on
        self._in_process = True
        self.is_init = False

        # start rosbridge client
        try:
            super().initialize(host, port)
        # pylint: disable=broad-except
        except Exception as e:
            self._logger.info('failure connecting to RosBridge server: %s', e)
            self._pipe[1].send(['error'])
            return
        else:
            self._pipe[1].send(['init'])

        # listen for proxy requests
        def make_callback(_msg):
            return lambda x: self._pipe[1].send([_msg[1], x])

        try:
            while True:
                msg = self._pipe[1].recv()
                if msg[0] == 'close':
                    self.close()
                    self._pipe[1].send(['close'])
                    break
                elif msg[0] == 'subscribe':
                    self.subscribe_topic(msg[1], msg[2], make_callback(msg))
                elif msg[0] == 'unsubscribe':
                    self.unsubscribe_topic(msg[1])
        # pylint: disable=broad-except
        except Exception as e:
            self._logger.info('Exception in RosBridge client process: %s', e)
            self._pipe[1].send(['error'])

    def _event_loop_proxy(self):
        """
        Method handling the communication from the RosBridge client process in a separate thread
        """
        while True:
            try:
                msg = self._pipe[0].recv()
                if msg[0] in self._callbacks:
                    self._callbacks[msg[0]](msg[1])
                elif msg[0] == 'init':
                    self.is_init = True
                elif msg[0] == 'close':
                    break
                elif msg[0] == 'error':
                    self.is_init = False
                    raise RosBridgeConnectError('Failure in RosBridge client process')
            except EOFError:
                self._logger.info('connection closed')
                break

    def subscribe_topic(self, name, ros_type, callback):
        """
        Subscribes a callback to a Ros topic

        :param name: string corresponding to the topic address
        :param ros_type: string corresponding to the topic type
        :param callback: function object to be called upon new message
        """
        if not self._is_init:
            self._logger.info('Rosbridge client was not correctly initialized. Could not subscribe '
                              'to: %s', name)
            return

        if self._in_process:
            super().subscribe_topic(name, ros_type, callback)
        else:
            # tell process to subscribe to topic
            self._callbacks[name] = callback
            self._pipe[0].send(['subscribe', name, ros_type])

    def unsubscribe_topic(self, name):
        """
        Unsubscribes a callback to a Ros topic

        :param name: string corresponding to the topic address
        """
        if not self._is_init:
            self._logger.info('Rosbridge client was not correctly initialized. Could not '
                              'unsubscribe from: %s', name)
            return

        if self._in_process:
            super().unsubscribe_topic(name)
        else:
            # tell process to unsubscribe from topic
            self._pipe[0].send(['unsubscribe', name])

    def close(self):
        """
        Closes the RosBridge connection. After this the handler can not be initialized again.
        Furthermore, it is not recommended to initialized any other client in the same process.
        Use class RosBridgeHandlerProcess if you need to do that.
        """
        if not self._is_init:
            self._logger.info('Rosbridge client was not correctly initialized. Cannot be closed')
            return

        if self._in_process:
            super().close()
        else:
            # tell process to shutdown
            self._pipe[0].send(['close'])
            self._callbacks = {}
            self.is_init = False
