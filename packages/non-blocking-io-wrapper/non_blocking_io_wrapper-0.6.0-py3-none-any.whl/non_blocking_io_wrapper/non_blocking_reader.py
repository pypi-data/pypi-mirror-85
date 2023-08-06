#  Copyright (c) 2020 SBA - MIT License

import io
import threading
from typing import Optional


class NonBlockingReader(io.RawIOBase):
    """Lightweight wrapper to create a non blocking version of any (byte) stream.

    It is a true io.RawIOBase subclass. Because of that, any method valid
    on an input byte stream should work seamlessly. Yet, a line access
    (readline, or iterator) will raise an OSError if no data is available at
    call time (you can use the `select` method to test/wait for
    that condition). If some data is available a line will be returned, or a
    partial one if no newline is available in the buffer.

    If no data is present, a read will return None instead of blocking.
    """
    def __init__(self, stream):
        self.stream = stream
        self.t = threading.Thread(target=self._get_data, name='get_data',
                                  daemon=True)
        self.lock = threading.Lock()
        self.available = threading.Event()
        self.data = []
        self.ended = False
        self.t.start()

    def readable(self) -> bool:
        return True

    def readinto(self, __buffer: bytearray) -> Optional[int]:
        with self.lock:
            if len(self.data) == 0:
                return 0 if self.ended else None
            begin = 0
            mx = len(__buffer)
            for i, block in enumerate(self.data):
                if mx == 0:
                    break
                if len(block) < mx:
                    ln = len(block)
                    __buffer[begin: begin + ln] = block
                    begin += ln
                    mx -= ln
                else:
                    __buffer[begin:] = block[:mx]
                    self.data[i] = block[mx:]
                    begin += mx
                    i -= 1
                    break
            if i >= 0:
                del self.data[:i + 1]
            if len(self.data) == 0:
                self.available.clear()
            return begin

    def _get_data(self):
        """A thread that continuously reads the underlying stream."""
        while not (self.closed or self.ended):
            block = self.stream.read(8192)
            with self.lock:
                if len(block) == 0:
                    self.ended = True
                else:
                    self.data.append(block)
                    self.available.set()

    def drain(self, timeout=None):
        """Waits for the underlying stream to reach its end of file.

        If timeout is given and is not None it is the maximum time in
        seconds to wait.
        Returns True if it succeeded or False on timeout.
        """
        self.t.join(timeout)
        return not self.t.is_alive()

    def __del__(self):
        self.close()
        super().__del__()

    def select(self, timeout=None):
        """Waits for data to become available, or more exactly for the
        next read not to return None. Specifically, it returns True after
        end of file has been reached, because the next read will
        immediately return b''.

        If timeout is given and is not None it is the maximum time in
        seconds to wait.
        Returns True if it succeeded or False on timeout.
        """
        if self.ended:
            return True
        self.available.wait(timeout)
        with self.lock:
            return 0 != len(self.data)
