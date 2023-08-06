from typing import Optional, Any


def strtobool(s: Any) -> Optional[bool]:
    """
    Convert a string into a boolean value or None

    True is returned when yes, true or 1 is called
    False is returned when no, false or 0 is called
    None is returned on any other value, we do this because we want to know if we are passing an
    invalid value
    """
    if s is None:
        return None
    if s.lower() in ("yes", "true", "1", "on"):
        return True
    elif s.lower() in ("no", "false", "0", "off"):
        return False
    else:
        return None


def msg(s: Any) -> None:
    """Print a message with a green-colored >>> signs

    This uses ANSI escape codes, if your terminal doesn't support them please
    switch to a sane terminal.

    Args:
        s (str): message to be printed
    """
    for line in str(s).splitlines():
        print("\033[1;32m>>>\033[1;0m {}".format(line))


def warn(s: Any) -> None:
    """Print a messsage with yellow-colored >>> signs

    This uses ANSI escape codes, if your terminal doesn't support them please
    switch to a sane terminal.

    Args:
        s (str): message to be printed
    """
    for line in str(s).splitlines():
        print("\033[1;33m>>> WARNING:\033[1;0m {}".format(line))


def err(s: Any) -> None:
    """Print a messsage with red-colored >>> signs

    This uses ANSI escape codes, if your terminal doesn't support them please
    switch to a sane terminal.

    Args:
        s (str): message to be printed
    """
    for line in str(s).splitlines():
        print("\033[1;31m>>> ERROR:\033[1;0m {}".format(line))
