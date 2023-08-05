#!/usr/local/bin/python3

"""AppStore Class"""

# PyLint cannot properly find names inside Cocoa libraries, so issues bogus
# No name 'Foo' in module 'Bar' warnings. Disable them.
# pylint: disable=no-name-in-module

import os
import sys
import syslog
from AppKit import (  # type: ignore
    NSAlert, NSInformationalAlertStyle, NSApp,
    NSOpenPanel, NSURL,
    NSURLBookmarkResolutionWithSecurityScope,
    NSURLBookmarkCreationWithSecurityScope,
    NSUserDefaults
)
import things3.things3_app
import things3


class Alert():  # pylint: disable=too-few-public-methods
    """Alert"""

    def __init__(self, message_text):
        super(Alert, self).__init__()
        self.message_text = message_text
        self.informative_text = ""
        self.buttons = []
        self.button_pressed = None

    def display_alert(self):
        """Alert"""
        alert = NSAlert.alloc().init()
        alert.setMessageText_(self.message_text)
        alert.setInformativeText_(self.informative_text)
        alert.setAlertStyle_(NSInformationalAlertStyle)
        for button in self.buttons:
            alert.addButtonWithTitle_(button)
        NSApp.activateIgnoringOtherApps_(True)
        self.button_pressed = alert.runModal()


class Things3Appstore():
    """Appstore"""
    DOMAIN = "dbpath"

    def __init__(self):
        self.db_file = things3.things3.Things3().database

    @staticmethod
    def alert(message="Default Message", info_text="", buttons=None):
        """Alert"""
        window = Alert(message)
        window.informative_text = info_text
        window.buttons = ["OK"] if buttons is None else buttons
        window.display_alert()
        return window.button_pressed

    def request_access(self):
        """NSOpen"""
        file_types = ['sqlite3']
        panel = NSOpenPanel.openPanel()
        panel.setCanCreateDirectories_(False)
        panel.setCanChooseDirectories_(True)
        panel.setCanChooseFiles_(False)
        panel.setTitle_("Allow Access to Folder")
        panel.setAllowedFileTypes_(file_types)
        path = os.path.dirname(self.db_file)
        self.debug(f"Requesting: {path}")
        my_url = NSURL.fileURLWithPath_isDirectory_(path, True)
        panel.setDirectoryURL_(my_url)

        panel.runModal()
        return panel.filename()

    def store_access_token(self, url):
        """Store"""
        # ObjC Example: https://stackoverflow.com/questions/13729958
        # PyObC Resource: https://stackoverflow.com/questions/21244781/
        # PyObC Resource: https://stackoverflow.com/questions/48862093
        url = NSURL.fileURLWithPath_(url)

        defaults = NSUserDefaults.standardUserDefaults()
        options = NSURLBookmarkCreationWithSecurityScope
        bookmark_data, error = url.bookmarkDataWithOptions_includingResourceValuesForKeys_relativeToURL_error_(  # noqa # pylint: disable=line-too-long
            options, None, None, None)
        self.debug(f"Bookmark Store Error Code: {error}")
        defaults.setObject_forKey_(bookmark_data, self.DOMAIN)

    def restore_access_token(self):
        """Restore"""
        # ObjC Example: https://stackoverflow.com/questions/13729958
        # PyObC Resource: https://stackoverflow.com/questions/21244781/
        # PyObC Resource: https://stackoverflow.com/questions/48862093
        defaults = NSUserDefaults.standardUserDefaults()
        bookmark_data = defaults.objectForKey_(self.DOMAIN)
        opts = NSURLBookmarkResolutionWithSecurityScope
        bookmark_file_url, stale, error = NSURL.URLByResolvingBookmarkData_options_relativeToURL_bookmarkDataIsStale_error_(  # noqa # pylint: disable=line-too-long
            bookmark_data, opts, None, None, None)
        self.debug(f"Bookmark Stale: {stale}")
        self.debug(f"Bookmark URL: {bookmark_file_url}")
        self.debug(f"Bookmark Read Error Code: {error}")
        if bookmark_file_url is not None:
            access = bookmark_file_url.startAccessingSecurityScopedResource()
            self.debug(f"Bookmark access: {access}")

    @staticmethod
    def debug(message):
        """Logging"""
        syslog.openlog("KanbanView")
        print(message)
        syslog.syslog(syslog.LOG_ALERT, message)

    def main(self):
        """Main"""
        path = self.db_file

        try:
            self.debug(f"Opening database: {self.db_file}")
            self.restore_access_token()
            with open(self.db_file):
                pass
        except IOError as error:
            self.debug(
                f"No access to database: {self.db_file}. Details: {error}")
            button = Things3Appstore.alert(
                "Allow Access to Folder",
                "Please allow the app to read the Things 3 database " +
                "by providing access to it on the next file dialog once. " +
                "In case we can't find your todos, " +
                "your documents folder will be shown on the next dialog and "
                "we'll use a demo database.",
                ["OK", "Cancel"])
            ok_button = 1000
            if button != ok_button:
                self.debug("User cancelled first prompt")
                sys.exit(0)

            path = self.request_access()
            self.debug(f"User selected {path}")
            try:
                self.debug(f"Opening again database: {self.db_file}")
                with open(self.db_file):
                    pass
                self.store_access_token(path)
            except IOError as error:
                # except FileNotFoundError as error:
                self.debug(
                    f"Database not found: {self.db_file}. Details: {error}")
                # self.alert("Thank you",
                #            "Thank you for providing access. " +
                #            "However, as we couldn't find or open " +
                #            "your Things 3 todos, " +
                #            "we're now opening a demo database.",
                #            ["OK"])
                self.db_file = os.getcwd() + "/resources/demo.sqlite3"
                self.debug(f"Using: {self.db_file}")
            # except IOError as error:
                # self.debug(
                #     f"Still no access to database: {self.db_file}. " +
                #     f"Details: {error}")
                # self.alert("No Access to Folder",
                #            "Can't open database. Please provide feedback " +
                #            "to support@kanbanview.app.",
                #            ["OK"])
                # sys.exit(1)

        things3.things3_app.Things3App(database=self.db_file).main(True)


if __name__ == '__main__':
    Things3Appstore().main()
