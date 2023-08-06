#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python Team Awareness Kit (PyTAK) Module Class Definitions."""

import asyncio
import logging
import os
import queue
import random
import socket
import threading
import time
import urllib

import pytak
import pycot

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2020 Orion Labs, Inc."
__license__ = "Apache License, Version 2.0"


# Dear Reader, Py3 doesn't need to inherit from Object anymore!
class NetworkClient:
    """CoT Network Client (TX)."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(pytak.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(pytak.LOG_LEVEL)
        _console_handler.setFormatter(pytak.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def __init__(self, cot_host: str, cot_port: int = None,
                 broadcast: bool = False) -> None:
        self.broadcast = broadcast

        self.socket: socket.socket = None
        self.addr: str = None
        self.port: int = None

        if ':' in cot_host:
            self.addr, port = cot_host.split(':')
            self.port = int(port)
        elif cot_port:
            self.addr = cot_host
            self.port = int(cot_port)
        else:
            self.addr = cot_host
            self.port = int(pytak.DEFAULT_COT_PORT)

        self.socket_addr = f'{self.addr}:{self.port}'

        if self.broadcast:
            self._logger.info(
                'Using Broadcast Socket, CoT Destination: %s',
                self.socket_addr)
            self._setup_broadcast_socket()
        else:
            self._logger.info(
                'Using Unicast Socket, CoT Destination: %s',
                self.socket_addr)
            self._setup_unicast_socket()

    def _setup_unicast_socket(self) -> None:
        """Sets up the TCP Unicast Socket for sending CoT events."""
        self._logger.debug(
            'Setting up Unicast Socket to CoT Destination: %s',
            self.socket_addr)
        if self.socket is not None:
            self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.addr, self.port))

    def _setup_broadcast_socket(self) -> None:
        """Sets up the UDP Broadcast Socket for sending CoT events."""
        self._logger.debug(
            'Setting up Broadcast Socket to CoT Destination: %s',
            self.socket_addr)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send_cot(self, event: bytes, timeout: int = 10) -> bool:
        """Wrapper for sending TCP Unicast or UDP Broadcast CoT Events."""
        if os.environ.get('DONT_ADD_NEWLINE'):
            _event = event
        else:
            _event = event + b'\n'

        self._logger.debug('Sending CoT to %s: "%s"', self.socket_addr, _event)

        if self.broadcast:  # pylint: disable=no-else-return
            return self.sendto(_event)
        else:
            return self.sendall(_event, timeout)

    def close(self):
        """Closes this instance's network socket."""
        return self.socket.close()

    def sendall(self, event: bytes, timeout: int = 10) -> bool:
        """Sends a CoT Event to a TCP Unicast address."""
        # is the socket alive?
        if self.socket.fileno() is -1:
            self._logger.warning(
                'Restarting Socket as socket.fileno() returned -1')
            self._setup_unicast_socket()
            return False

        self.socket.settimeout(timeout)

        try:
            self.socket.sendall(event)
            if not os.environ.get('DISABLE_RANDOM_SLEEP'):
                time.sleep(pytak.DEFAULT_SLEEP * random.random())
            return True
        except Exception as exc:
            self._logger.error(
                'socket.sendall() raised an Exception, sleeping: ')
            self._logger.exception(exc)
            time.sleep(pytak.DEFAULT_BACKOFF * random.random())
            self._setup_unicast_socket()
            return False

    def sendto(self, event: bytes) -> bool:
        """Sends a CoT Event to a UDP Broadcast address."""
        try:
            self.socket.sendto(event, (self.addr, self.port))
            return True
        except Exception as exc:
            self._logger.error(
                'socket.sendto() raised an Exception, sleeping: ')
            self._logger.exception(exc)
            time.sleep(pytak.DEFAULT_BACKOFF * random.random())
            self._setup_broadcast_socket()
            return False


class CoTWorker(threading.Thread):

    """CoTWorker Thread."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(pytak.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(pytak.LOG_LEVEL)
        _console_handler.setFormatter(pytak.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def __init__(self, msg_queue: queue.Queue, cot_host: str,
                 cot_port: int = None, broadcast: bool = False) -> None:
        self.msg_queue: queue.Queue = msg_queue

        self.net_client = NetworkClient(
            cot_host=cot_host,
            cot_port=cot_port,
            broadcast=broadcast
        )

        # Thread setup:
        threading.Thread.__init__(self)
        self.daemon = True
        self._stopper = threading.Event()

    def stop(self):
        """Stop the thread at the next opportunity."""
        self._logger.debug('Stopping CoTWorker')
        self.net_client.close()
        self._stopper.set()

    def stopped(self):
        """Checks if the thread is stopped."""
        return self._stopper.isSet()

    def run(self):
        """Runs this Thread, reads in Message Queue & sends out CoT."""
        self._logger.info('Running CoTWorker')

        while not self.stopped():
            try:
                msg = self.msg_queue.get(True, 1)
                self._logger.debug('From msg_queue: "%s"', msg)
                if not msg:
                    continue
                self.net_client.send_cot(msg)
            except queue.Empty:
                recv = self.net_client.socket.recv(1024)
                pass


class AsyncNetworkClient(asyncio.Protocol):
    """Async CoT Network Client (TX)."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(pytak.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(pytak.LOG_LEVEL)
        _console_handler.setFormatter(pytak.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False
    logging.getLogger('asyncio').setLevel(pytak.LOG_LEVEL)

    def __init__(self, msg_queue: queue.Queue, on_con_lost) -> None:
        self.transport = None
        self.msg_queue = msg_queue
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self._logger.debug('Connected to %s', self.address)

    def connection_lost(self, exc):
        self._logger.warning('Disconnected from %s', self.address)
        self._logger.exception(exc)
        self.on_con_lost.set_result(None)

    def error_received(self, exc):
        self._logger.warning('Disconnected from %s', self.address)
        self._logger.exception(exc)
        #if not self.on_con_lost.done():
        self.on_con_lost.set_result(None)

    def eof_received(self):
        self._logger.debug('Received EOF from %s', self.address)
        self.transport.close()
        #if not self.on_con_lost.done():
        self.on_con_lost.set_result(None)

    def wait_connection_lost(self):
        return self.on_con_lost.done()


class AsyncCoTWorker:

    """Async CoTWorker."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(pytak.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(pytak.LOG_LEVEL)
        _console_handler.setFormatter(pytak.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False
    logging.getLogger('asyncio').setLevel(pytak.LOG_LEVEL)

    def __init__(self, msg_queue: asyncio.Queue, transport) -> None:
        self.msg_queue = msg_queue
        self.transport = transport

    async def run(self):
        """Runs this Thread, reads in Message Queue & sends out CoT."""
        self._logger.info('Running AsyncCoTWorker')

        while 1:
            msg = await self.msg_queue.get()
            self._logger.debug('From msg_queue: "%s"', msg)
            if not msg:
                continue
            self.transport.write(msg)
            if not os.environ.get('DISABLE_RANDOM_SLEEP'):
                await asyncio.sleep(pytak.DEFAULT_SLEEP * random.random())


class EventWorker:

    """EventWorker."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(pytak.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(pytak.LOG_LEVEL)
        _console_handler.setFormatter(pytak.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False
    logging.getLogger('asyncio').setLevel(pytak.LOG_LEVEL)

    def __init__(self, event_queue: asyncio.Queue, writer) -> None:
        self.event_queue = event_queue
        self.writer = writer

    async def run(self):
        """Runs this Thread, reads in Message Queue & sends out CoT."""
        self._logger.info('Running EventWorker')

        while 1:
            event = await self.event_queue.get()
            if not event:
                continue
            self._logger.debug("event='%s'", event)

            if isinstance(event, pycot.Event):
                _event = event.render(encoding='UTF-8', standalone=True)
            else:
                _event = event

            if hasattr(self.writer, "send"):
                await self.writer.send(_event)
            else:
                self.writer.write(_event)
                await self.writer.drain()
            if not os.environ.get('DISABLE_RANDOM_SLEEP'):
                await asyncio.sleep(pytak.DEFAULT_SLEEP * random.random())


class MessageWorker:

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(pytak.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(pytak.LOG_LEVEL)
        _console_handler.setFormatter(pytak.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False
    logging.getLogger('asyncio').setLevel(pytak.LOG_LEVEL)

    def __init__(self, event_queue: asyncio.Queue,
                 url: urllib.parse.ParseResult, cot_stale: int = None):
        self.event_queue = event_queue
        self.url = url
        self.cot_stale = cot_stale

    async def _put_event_queue(self, event: pycot.Event) -> None:
        """Puts Event onto the CoT Transmit Queue."""
        try:
            await self.event_queue.put(event)
        except queue.Full as exc:
            self._logger.warning(
                'Lost CoT Event (queue full): "%s"', _event)

    async def run(self) -> None:
        self._logger.info("Overwrite this method!")
        pass
