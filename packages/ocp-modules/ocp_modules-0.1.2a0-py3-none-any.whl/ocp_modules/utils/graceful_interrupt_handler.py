import signal

class GracefulInterruptHandler:
    """Registers a signal handler (default is SIGINT) and closes
    the context if a signal arrives. It can be used like so:
    with GracefulInterruptHandler() as handler:
        while not handler.interrupted:
            # do your stuff
    """

    def __init__(self, sig=signal.SIGINT):
        self.sig = sig

    def __enter__(self):
        self.interrupted = False
        self.released = False
        self.original_handler = signal.getsignal(self.sig)

        def handler(signum, frame):
            self.release()
            self.interrupted = True

        signal.signal(self.sig, handler)
        return self

    def __exit__(self, type, value, tb):
        self.release()

    def release(self):
        if self.released:
            return False

        signal.signal(self.sig, self.original_handler)
        self.released = True
        return True
