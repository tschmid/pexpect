#!/usr/bin/env python
import pexpect
import unittest
import PexpectTestCase
import time
import os

class TestCaseMisc(PexpectTestCase.PexpectTestCase):
        
    def test_isatty (self):
        child = pexpect.spawn('cat')
        assert child.isatty(), "Not returning True. Should always be True."
    def test_read (self):
        child = pexpect.spawn('cat')
        child.sendline ("abc")
        child.sendeof()
        assert child.read(0) == '', "read(0) did not return ''"
        assert child.read(1) == 'a', "read(1) did not return 'a'"
        assert child.read(1) == 'b', "read(1) did not return 'b'"
        assert child.read(1) == 'c', "read(1) did not return 'c'"
        assert child.read(2) == '\r\n', "read(2) did not return '\\r\\n'"
        assert child.read() == 'abc\r\n', "read() did not return 'abc\\r\\n'"
    def test_readline (self):
        child = pexpect.spawn('cat')
        child.sendline ("abc")
        child.sendline ("123")
        child.sendeof()
        assert child.readline(0) == '', "readline(0) did not return ''"
        assert child.readline() == 'abc\r\n', "readline() did not return 'abc\\r\\n'"
        assert child.readline(2) == 'abc\r\n', "readline(2) did not return 'abc\\r\\n'"
        assert child.readline(1) == '123\r\n', "readline(1) did not return '123\\r\\n'"
        assert child.readline() == '123\r\n', "readline() did not return '123\\r\\n'"
    def test_iter (self):
        child = pexpect.spawn('cat')
        child.sendline ("abc")
        child.sendline ("123")
        child.sendeof()
        # Don't use "".join() because we want to test the ITERATOR.
        page = ""
        for line in child:
            page = page + line
        assert page == 'abc\r\nabc\r\n123\r\n123\r\n', "iterator did not work. page=%s"%repr(page)
    def test_readlines(self):
        child = pexpect.spawn('cat')
        child.sendline ("abc")
        child.sendline ("123")
        child.sendeof()
        page = child.readlines()
        page = ''.join(page)
        assert page == 'abc\r\nabc\r\n123\r\n123\r\n', "readlines() did not work. page=%s"%repr(page)
    def test_write (self):
        child = pexpect.spawn('cat')
        child.write('a')
        child.write('\r')
        assert child.readline() == 'a\r\n', "write() did not work"
    def test_writelines (self):
        child = pexpect.spawn('cat')
        child.writelines(['abc','123','xyz','\r'])
        child.sendeof()
        line = child.readline()
        assert line == 'abc123xyz\r\n', "writelines() did not work. line=%s"%repr(line)
    def test_eof(self):
        child = pexpect.spawn('cat')
        child.sendeof()
        try:
            child.expect ('the unexpected')
        except:
            pass
        assert child.eof(), "child.eof() did not return True"
    def test_terminate(self):
        child = pexpect.spawn('cat')
        child.terminate(force=1)
        assert child.terminated, "child.terminated is not True"
    def test_bad_child_pid(self):
        child = pexpect.spawn('cat')
        child.terminate(force=1)
        child.terminated = 0 # Force invalid state to test code
        try:
            child.isalive()
        except pexpect.ExceptionPexpect, e:
            pass
        except:
            self.fail ("child.isalive() should have raised a pexpect.ExceptionPexpect")
        child.terminated = 1 # Force back to valid state so __del__ won't complain
    def test_isalive(self):
        child = pexpect.spawn('cat')
        assert child.isalive(), "child.isalive() did not return True"
        child.sendeof()
        child.expect(pexpect.EOF)
        assert not child.isalive(), "child.isalive() did not return False"
    def test_bad_type_in_expect(self):
        child = pexpect.spawn('cat')
        try:
            child.expect({}) # We don't support dicts yet. Should give TypeError
        except TypeError, e:
            pass
        except:
            self.fail ("child.expect({}) should have raised a TypeError")
    def test_winsize(self):
        child = pexpect.spawn('cat')
        child.setwinsize(10,13)
        assert child.getwinsize()==(10,13), "getwinsize() did not return (10,13)"
    def test_which (self):
        p = os.defpath
        ep = os.environ['PATH']
        os.defpath = ":/tmp"
        os.environ['PATH'] = ":/tmp"
        wp = pexpect.which ("ticker.py")
        assert wp == 'ticker.py', "Should return a string. Returned %s" % wp
        os.defpath = "/tmp"
        os.environ['PATH'] = "/tmp"
        wp = pexpect.which ("ticker.py")
        assert wp == None, "Executable should not be found. Returned %s" % wp
        os.defpath = p
        os.environ['PATH'] = ep
        
if __name__ == '__main__':
    unittest.main()

suite = unittest.makeSuite(TestCaseMisc,'test')

