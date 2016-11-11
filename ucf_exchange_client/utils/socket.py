import socket


def get_conn(host, port):
    """Return a file-like socket object."""
    pass

def get_msg(sock):
    """Read one complete message from socket."""
    # basically, block and read until newline, or complete JSON, or whatever.
    # then marshal into our message type.
    pass
