#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""KanbanView (app) for Things 3."""

from __future__ import print_function

# pylint: disable=duplicate-code
__author__ = "Alexander Willner"
__copyright__ = "Copyright 2020 Alexander Willner"
__credits__ = ["Luc Beaulieu", "Alexander Willner"]
__license__ = "Apache License 2.0"
__version__ = "2.6.3"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import sys
import signal
from os import system
from threading import Thread
import webview  # type: ignore
import objc  # type: ignore # pylint: disable=unused-import # noqa F401
import pkg_resources.py2_warn  # type: ignore # pylint: disable=unused-import # noqa F401
import things3.things3_api as things3_api


class Things3App():
    """App wrapper for simple read-only API for Things 3."""

    database = None
    FILE = "kanban.html"
    api = None
    api_thread = None

    def open_api(self):
        """Delay opening the browser."""
        print(f"Using database 2: {self.database}")
        self.api.main()

    def __init__(self, database=None):
        self.database = database
        self.api = things3_api.Things3API(database=self.database)

    def sigterm_handler(self, _signo, _stack_frame):
        """Make sure the server shuts down."""
        print("Sigterm...")
        self.api.flask_context.shutdown()

    def main(self, appstore=False):
        """Run the app."""
        # kill possible zombie processes; can't use psutil in py2app context
        system('lsof -nti:' + str(things3_api.Things3API.port) +
               ' | xargs kill -9')

        # Make sure the server shuts down
        signal.signal(signal.SIGTERM, self.sigterm_handler)

        print(f"Using database 1: {self.database}")

        window = webview.create_window(
            title='KanbanView',
            url=f'http://{things3_api.Things3API.host}:' +
            f'{things3_api.Things3API.port}/{self.FILE}',
            width=1280, height=650,
            min_size=(1280, 650),
            frameless=True)
        if not appstore:
            window.closed += advertise
        self.api_thread = Thread(target=self.open_api)

        try:
            self.api_thread.start()
            webview.start()  # blocking
            self.api.flask_context.shutdown()
            self.api_thread.join()
        except KeyboardInterrupt:
            print("Shutting down...")
            self.api.flask_context.shutdown()
            self.api_thread.join()
            sys.exit(0)


def advertise():
    """Show a hint to buy the app"""
    text = "Thank you for using KanbanView! " +\
        "If you enjoy using it, please consider buying the app."
    title = "KanbanView"
    url = "https://kanbanview.app"
    system("""osascript -e ' """ +
           f"""set dialog to (display dialog "{text}" """ +
           """buttons {"Buy", "Later"} default button 1 """ +
           f"""giving up after 10 """ +
           f"""with title "{title}" """ +
           f"""with icon POSIX file "resources/icon.icns")' """ +
           f"""-e 'if the button returned of the result is "Buy" then' """ +
           f"""-e 'do shell script "open {url}"' -e 'end if'""")


def main():
    """Main entry point for CLI installation"""
    Things3App().main()


if __name__ == "__main__":
    main()
