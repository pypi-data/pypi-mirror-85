#  Copyright (c) 2020 SBA - MIT License

from unittest import TestCase
from unittest.mock import Mock

import io
import time

from non_blocking_io_wrapper.non_blocking_reader import NonBlockingReader


class TimedRead:
    def __init__(self, *seq):
        self.seq = seq[:]
        self.it = iter(self.seq)

    def __call__(self, _hint=-1):
        try:
            delay, data = next(self.it)
        except StopIteration:
            return b''
        time.sleep(delay)
        return data


class TestNonBlockingReader(TestCase):
    def setUp(self) -> None:
        raw = Mock(io.RawIOBase)
        raw.read = Mock()
        raw.read.side_effect = TimedRead((.1, b'a'), (.1, b'b\nc'), (.1, b'd'))
        self.fd = NonBlockingReader(raw)

    def test_drain(self):
        self.fd.drain()
        self.assertEqual(b'ab\ncd', self.fd.read())

    def test_timed_read(self):
        self.assertIsNone(self.fd.read())
        time.sleep(.25)
        self.assertEqual(b'ab\nc', self.fd.read())

    def test_readline_no_data(self):
        with self.assertRaises(OSError):
            self.fd.readline()

    def test_readline_no_eol(self):
        time.sleep(.15)
        data = self.fd.readline()
        self.assertEqual(b'a', data)

    def test_readline_eol(self):
        time.sleep(.25)
        data = self.fd.readline()
        self.assertEqual(b'ab\n', data)

    def test_iter(self):
        self.fd.drain()
        self.assertEqual([b'ab\n', b'cd'], list(self.fd))

    def test_select_timeout(self):
        self.assertFalse(self.fd.select(.05))
        self.assertIsNone(self.fd.read())

    def test_select_ok(self):
        beg = time.time()
        self.assertTrue(self.fd.select(.5))
        end = time.time()
        self.assertEqual(b'a', self.fd.read())
        self.assertTrue(.05 < end-beg < .15)

    def test_select_eof(self):
        self.fd.drain()
        self.assertEqual(b'ab\ncd', self.fd.read())
        beg = time.time()
        self.assertTrue(self.fd.select(.1))
        end = time.time()
        self.assertTrue(end-beg < .05)
        self.assertEqual(b'', self.fd.read())
