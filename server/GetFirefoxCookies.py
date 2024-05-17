import argparse
import fnmatch
import json
import os
import os.path
import sqlite3
import sys
from collections import namedtuple

import lz4.block


class FirefoxCookieError(Exception):
    pass


class FirefoxSessionStoreMissingError(FirefoxCookieError):
   pass


# {{{1 mozLz4 decoding
#
# See:
# https://searchfox.org/mozilla-central/rev/05603d404851b5079c20c999890abe2f35a28322/dom/system/IOUtils.h#727

MOZLZ4_MAGIC = b'mozLz40\0'


class InvalidMozLz4FileError(FirefoxCookieError):
    pass


def read_mozlz4(file_path):
    with open(file_path, 'rb') as fh:
        if fh.read(len(MOZLZ4_MAGIC)) != MOZLZ4_MAGIC:
            raise InvalidMozLz4FileError(f'not an mozLz4 file: {file_path}')

        return lz4.block.decompress(fh.read())

# 1}}}


# {{{1 Cookie serialization
#
# See: https://everything.curl.dev/http/cookies/fileformat
#
# The header of a Netscape Cookie File is one of the following
# (according to http://fileformats.archiveteam.org/wiki/Netscape_cookies.txt):
#
# - "# HTTP Cookie File"
# - "# Netscape HTTP Cookie File"
#
# We choose the second one because the author likes it more.

COOKIE_JAR_HEADER = '# Netscape HTTP Cookie File'


class Cookie(
        namedtuple(
            'Cookie',
            'host allow_subdomains path is_secure expiry name value'
        )):
    __slots__ = ()

    def serialize(self):
        return '\t'.join(
            str(x) if not isinstance(x, bool) else str(x).upper()
            for x in self
        )


def write_cookie_jar(cookies, file_path):
    with open(
        file_path, 'w', encoding='utf-8', newline='\n',
        opener=lambda file, flags: os.open(file, flags, mode=0o600)
    ) as fh:
        fh.write(COOKIE_JAR_HEADER)
        fh.write('\n')
        
        for c in cookies:
            fh.write(c.serialize())
            fh.write('\n')

    os.chmod(file_path, 0o600)

# 1}}}


class FirefoxCookieReader:
    SESSIONSTORE_NAME = 'sessionstore.jsonlz4'
    COOKIEDB_NAME = 'cookies.sqlite'

    
    @staticmethod
    def _sqlite_convert_bool(bytes_obj):
        return bytes_obj != b'0'


    def __init__(self, profile_dir, host_glob_patterns=None):
        self._profile_dir = profile_dir
        self._host_globs = frozenset(host_glob_patterns or [])

        sqlite3.register_converter('bool', self._sqlite_convert_bool)


    def _is_host_matched(self, host):
        if not self._host_globs:
            return True

        for p in self._host_globs:
            if fnmatch.fnmatchcase(host, p):
                return True

        return False


    def _iter_session_cookies(self):
        try:
            data = json.loads(
                read_mozlz4(
                    os.path.join(self._profile_dir, self.SESSIONSTORE_NAME)
                )
            )
        except OSError as e:
            raise FirefoxSessionStoreMissingError(
                f'Firefox session store "{e.filename}" not found. Close Firefox, and try again.'
            ) from e

        for c in data['cookies']:
            if not self._is_host_matched(c['host']):
                continue

            yield Cookie(
                host=c['host'],
                allow_subdomains=c['host'].startswith('.'),
                path=c['path'],
                is_secure=c.get('secure', False),
                expiry=0,  # Session cookie
                name=c.get('name', ''),  # Empty name ok says http.cookiejar (?!)
                value=c['value'],
            )


    def _iter_persisted_cookies(self):
        conn = None

        try:
            conn = sqlite3.connect(
                os.path.join(self._profile_dir, self.COOKIEDB_NAME),
                detect_types=sqlite3.PARSE_COLNAMES
            )

            cursor = conn.execute(
                '''
                SELECT
                    host,
                    host LIKE '.%' AS 'allow_subdomains [bool]',
                    path,
                    isSecure AS 'isSecure [bool]',
                    expiry,
                    name,
                    value
                FROM moz_cookies;
                '''
            )

            for row in cursor:
                c = Cookie._make(row)
                if not self._is_host_matched(c.host):
                    continue

                yield c
        finally:
            if conn:
                conn.close()


    def __iter__(self):
        yield from self._iter_session_cookies()
        yield from self._iter_persisted_cookies()


def get_argparser():
    p = argparse.ArgumentParser(
        description='Dump cookies from Firefox, as a Netscape Cookie File.'
    )

    p.add_argument(
        '-l', '--host-limit',
        metavar='GLOB_PATTERN',
        action='append',
        help='Only dump cookies for hosts matching the glob pattern. Can be specified multiple times. Example: '
             '*.example.com'
    )

    p.add_argument(
        'firefox_profile_dir',
        help='Path to Firefox profile directory.'
    )
    
    p.add_argument(
        'output_file',
        help='Path to the output file.'
    )

    return p


def main():
    args = get_argparser().parse_args()

    cookie_reader = FirefoxCookieReader(args.firefox_profile_dir, args.host_limit)

    write_cookie_jar(cookie_reader, args.output_file)


if __name__ == '__main__':
    sys.exit(main())