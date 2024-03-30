import pickle
import bz2
import datetime

# Constants
ENTRY_SEPARATOR = b"fHwwYjExMDF8MHhERUFEQkVFRnx8"
SESSION_SEPARATOR = b"fDVFNTUxMDd8"
FILEPATH = "log.bin"

# Open log
decoded_sessions: dict[str, list[dict[str, str | int | float]]] = {"sessions": []}
with open(FILEPATH, "rb") as file:
    # Extract sessions
    sessions: list[bytes] = file.read().split(SESSION_SEPARATOR)

    # Retrieve entries for each session
    for session in sessions:
        # Skip blank sessions
        if session == b"":
            continue

        # Extract entries
        entries: list[bytes] = session.split(ENTRY_SEPARATOR)
        print(f"New session ({len(entries) - 1} events logged)")

        # Output individual entries
        decoded_entries: list[dict[str, str | int | float]] = []
        for entry in entries[:-1]:
            # Skip blank entries
            if entry == b"":
                continue

            # Decode entry
            decoded_entry: dict[str, str | int | float] = pickle.loads(
                bz2.decompress(entry)
            )
            decoded_entry["time"] = str(
                datetime.datetime.fromtimestamp(decoded_entry["time"]) # type: ignore
            )

            # Print it out
            print(decoded_entry)

        # Formatting stuff below
        print()
    print(f"Total: {len(sessions) - 1} sessions")
