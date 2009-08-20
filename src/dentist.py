import re
import pwd
import logging


class FileWatcher(object):

    def __init__(self, path, reader):
        self.file = open(path, 'rb')
        self.reader = reader

    def read_line(self):
        line = self.file.readline()
        user = self.reader.check_line(line)
        if user is not None:
            self.write_to_user(user, line)

    def write_to_user(self, user, line):
        logging.debug('Writing to %s : %s' % (user, line))
        pass


class CombinedLogReader(object):
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
    REGEX = r'^([^ ]+) ([^ ]+) ([^ ]+) \[([^]]+)\] "([^ ]+) ([^ ]+) ([^ ]+)" ?(.*)$'
    REGEX_C = re.compile(REGEX)

    @classmethod
    def check_line(cls, line):
        uri = cls.parse_uri(line)
        if uri is not None:
           user = cls.parse_user(uri)
           if user is not None:
               if cls.user_exists(user):
                   return user

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
        >>> clr.parse_user('/home/abc')
        'abc'
        >>> clr.parse_user('/home/abc/index.html')
        'abc'
        >>> clr.parse_user('/~abc')
        'abc'
        >>> clr.parse_user('/~abc/index.html')
        'abc'
        >>> clr.parse_user('/')
        >>> clr.parse_user('/otherstuff')
        """
        if uri.startswith('/home/'):
            user = uri.split('/', 3)[2]
            return user
        if uri.startswith('/~'):
            x = uri.split('~', 1)[1]
            y = x.split('/', 1)
            return y[0]

    @classmethod
    def user_exists(cls, user):
        try:
            pwent = pwd.getpwnam(user)
            return True
        except KeyError:
            return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()
