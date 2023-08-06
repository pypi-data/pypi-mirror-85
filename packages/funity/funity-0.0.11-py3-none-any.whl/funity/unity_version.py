#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations


class UnityVersion(object):

    major: int
    minor: int
    patch: int
    build: int

    def __init__(self, major: int, minor: int, patch: int = 0, build: int = 0):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.build = build

    def __repr__(self):
        return f'{self.major}.{self.minor}.{self.patch}f{self.build}'

    def __eq__(self, other: UnityVersion):
        return (self.major, self.minor, self.patch, self.build) == (other.major, other.minor, other.patch, other.build)

    def __gt__(self, other: UnityVersion):
        return (self.major, self.minor, self.patch, self.build) > (other.major, other.minor, other.patch, other.build)

    @staticmethod
    def is_equal(first: UnityVersion, second: UnityVersion, fuzzy: bool = True) -> bool:
        if not fuzzy:
            return first == second
        return (first.major, first.minor) == (second.major, second.minor)

    def is_equal_to(self, other: UnityVersion, fuzzy: bool = True) -> bool:
        return UnityVersion.is_equal(self, other, fuzzy)
