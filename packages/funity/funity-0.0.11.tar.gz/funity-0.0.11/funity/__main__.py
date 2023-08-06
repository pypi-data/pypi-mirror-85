#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import getcwd
from pathlib import Path

from funity import UnityEditor


def main():
    cache_dir = Path(getcwd()) / 'editor.cache'

    # Find all Unity editor installations and cache the results into 'cache_dir'.
    editors = UnityEditor.find_in(cache=str(cache_dir))

    print(editors)


if __name__ == '__main__':
    main()
