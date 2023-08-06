#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from subprocess import PIPE, STDOUT, Popen
from typing import Callable, List

from funity import __name__ as module_name

_logger = None


def _acquire_logger():
    return logging.getLogger(module_name)


def get_logger():
    global _logger

    if not _logger:
        _logger = _acquire_logger()

    return _logger


def run_process(command: List[str],
                log_func: Callable[[str], None] = None) -> int:
    if log_func is not None:
        log_func(f': >> Running subprocess.. {" ".join(command)}\n')
    with Popen(command,
               stderr=STDOUT,
               stdout=PIPE,
               universal_newlines=True) as process:
        for line in process.stdout:
            if log_func is not None:
                log_func(f': {line}')
    return_code = process.returncode
    if log_func is not None:
        log_func(f': >> Subprocess finished with exit code {return_code}\n')

    return return_code
