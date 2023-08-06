# coding=utf-8

import os

from .matcher import Matcher, MatcherError
from .util import convert2pass


class LocMatcher:
    def __init__(self):
        self._normal_matcher = None
        self._location_matcher = None

    def load_from_file(self, path):
        if self._normal_matcher or self._location_matcher:
            raise MatcherError("matcher is initialized")
        if not os.path.isfile(path):
            return False

        normal_patterns = list()
        location_patterns = list()
        with open(path) as fp:
            for line in fp.readlines():
                if not line:
                    continue
                if line[-1] == "\n":
                    line = line[:-1]
                pattern = line.split("\t", 1)[0]
                if "[:loc:]" in pattern:
                    location_patterns.append(line)
                else:
                    normal_patterns.append(line)

        self._normal_matcher = Matcher.create_by_collection(normal_patterns)
        self._location_matcher = Matcher.create_by_collection(location_patterns)
        return self._normal_matcher is not None and self._location_matcher is not None

    @classmethod
    def create_by_file(cls, path):
        matcher = cls()
        if matcher.load_from_file(path):
            return matcher
        return None

    def load_from_collection(self, strings):
        if self._normal_matcher or self._location_matcher:
            raise MatcherError("matcher is initialized")
        if isinstance(strings, list) or isinstance(strings, set):
            # for utf-8 '\n' is 0x0a, in other words, utf-8 is ascii compatible.
            # but in python3, str.join is only accept str as argument

            normal_patterns = list()
            location_patterns = list()

            for word in strings:
                word = convert2pass(word)
                pattern = word.split("\t", 1)[0]
                if "[:loc:]" in pattern:
                    location_patterns.append(word)
                else:
                    normal_patterns.append(word)
        else:
            raise MatcherError("should be list or set")

        self._normal_matcher = Matcher.create_by_collection(normal_patterns)
        self._location_matcher = Matcher.create_by_collection(location_patterns)
        return self._normal_matcher is not None and self._location_matcher is not None

    @classmethod
    def create_by_collection(cls, strings):
        matcher = cls()
        if matcher.load_from_collection(strings):
            return matcher
        return None

    def findall(self, content, loc_content=None):
        matched = self._normal_matcher.findall(content)
        if loc_content is not None:
            matched.extend(self._location_matcher.findall(loc_content))
            matched.sort(lambda a, b: a[2] - b[2] if a[1] == b[1] else a[1] - b[1])
        return matched

    def finditer(self, content, loc_content=None):
        return iter(self.findall(content, loc_content))

    def search(self, content, loc_content=None):
        """Return first matched.

        :type content: str
        :rtype: (str, int, int, str)
        """
        ctx = self.finditer(content, loc_content)
        for matched in ctx:
            return matched
        return None
