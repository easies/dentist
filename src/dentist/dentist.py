import re
import pwd
import logging
import time
import os


class LogReader(object):
    output_directory = '/tmp'

    @classmethod
    def set_output_directory(cls, path):
        cls.output_directory = path

    @classmethod
    def get_info(cls, user):
        """
        >>> pwd.getpwnam('root') is not None
        True
        """
        try:
            return pwd.getpwnam(user)
        except KeyError:
            return None

    @classmethod
    def check_line(cls, line):
        raise NotImplementedError


class CombinedLogReader(LogReader):
    """Parse Apache logs in the combined format.
    "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\" \\"%{User-agent}i\\"
    """

    # 1 = Remote host
    # 2 = remote ident
    # 3 = ?
    # 4 = date
    # 5 = HTTP Request, (GET, POST, etc.)
    # 6 = URI
    # 7 = HTTP version
    # 8 = Rest
    REGEX = (r'^([^ ]+) ([^ ]+) ([^ ]+) \[([^]]+)\] '
             r'"([^ ]+) ([^ ]+) ([^ ]+)" ?(.*)$')
    REGEX_C = re.compile(REGEX)
    prefixes = ['/~']

    @classmethod
    def add_prefix(cls, *args):
        """
        >>> cls = CombinedLogReader
        >>> '/~' in cls.prefixes
        True
        >>> cls.add_prefix('abc', 'xyz')
        >>> 'abc' in cls.prefixes
        True
        >>> 'xyz' in cls.prefixes
        True
        """
        cls.prefixes += args

    @classmethod
    def check_line(cls, line):
        uri = cls.parse_uri(line)
        if uri is not None:
            user = cls.parse_user(uri)
            if user is not None:
                return cls.get_info(user)

    @classmethod
    def parse_uri(cls, line):
        m = cls.REGEX_C.match(line)
        if m is not None:
            uri = m.group(6)
            return uri

    @classmethod
    def parse_user(cls, uri):
        """
        >>> clr = CombinedLogReader()
        >>> clr.parse_user('')
        >>> clr.parse_user('/')
        >>> clr.parse_user('/otherstuff')
        >>> clr.parse_user('/~abc')
        'abc'
        >>> clr.parse_user('/~abc/index.html')
        'abc'
        >>> clr.parse_user('/home/abc')
        >>> clr.parse_user('/home/abc/index.html')
        >>> clr.add_prefix('/home/')
        >>> clr.parse_user('/home/abc')
        'abc'
        >>> clr.parse_user('/home/abc/index.html')
        'abc'
        """
        for p in cls.prefixes:
            if uri.startswith(p):
                s = uri[len(p):]
                return s.split('/', 1)[0]


class ErrorLogReader(LogReader):
    HOMEDIR_ROOT = '/home'
    HOMEDIR_ROOT_LEN = len(HOMEDIR_ROOT)

    @classmethod
    def configure(cls, **kwargs):
        """
        >>> ErrorLogReader.HOMEDIR_ROOT
        '/home'
        >>> ErrorLogReader.configure()
        >>> ErrorLogReader.HOMEDIR_ROOT
        '/home'
        >>> ErrorLogReader.configure(homedir_root='/other/home')
        >>> ErrorLogReader.HOMEDIR_ROOT
        '/other/home'
        """
        try:
            cls.HOMEDIR_ROOT = kwargs['homedir_root']
            cls.HOMEDIR_ROOT_LEN = len(cls.HOMEDIR_ROOT)
        except KeyError:
            pass

    @classmethod
    def check_line(cls, line):
        index = line.find(HOMEDIR_ROOT)
        if index < 0:
            return

        index += HOMEDIR_ROOT_LEN
        user = line[index:].split('/', 1)[0].split(' ')[0]
        return cls.get_info(user)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
