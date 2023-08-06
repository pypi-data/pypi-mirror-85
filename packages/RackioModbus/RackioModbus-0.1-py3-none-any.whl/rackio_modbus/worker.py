# -*- coding: utf-8 -*-
"""rackio_socket/core.py

This module implements the core app class and methods for Rackio Socket.
"""
import time

from threading import Thread


class ModbusWorker(Thread):

    def __init__(self, app, mode, *args, **kwargs):

        super(ModbusWorker, self).__init__(*args, **kwargs)

        self.app = app
        self.mode = mode

    def run_client(self):

        while True:

            time.sleep(0.5)

    def run(self):

        try:
            if self.mode == "server":
                self.app.setup_bindings()
                self.app.setup_api()
                app = self.app.get_driver()
                app.serve_forever()
            else:
                self.run_client()
        finally:
            self.app.shutdown()
            self.app.server_close()
