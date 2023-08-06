#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from datetime import datetime
from json import dumps, loads
from os import chdir, getcwd, walk
from pathlib import Path
from platform import system
from re import match
from shutil import copyfile, move, rmtree
from typing import Callable, List, Tuple

from funity.unity_version import UnityVersion
from funity.util import run_process


def __find_darwin(search_dir: str) -> List[str]:
    search_path = Path(search_dir)
    editor_dirs = []
    for root, dirs, _ in walk(search_path):
        root_path = Path(root)
        if not root_path.name == 'Unity.app':
            continue
        dirs[:] = []
        editor_dirs.append(str(root_path.parent))

    return editor_dirs


def __find_linux(search_dir: str) -> List[str]:
    search_path = Path(search_dir)
    editor_dirs = []
    for root, dirs, files in walk(search_path):
        root_path = Path(root)
        if 'Editor' != root_path.name:
            continue
        if 'Unity' not in files:
            continue
        dirs[:] = []
        editor_dirs.append(str(root_path.parent))

    return editor_dirs


def __find_windows(search_dir: str) -> List[str]:
    search_path = Path(search_dir)
    editor_dirs = []
    for root, dirs, files in walk(search_path):
        root_path = Path(root)
        if 'Editor' != root_path.name:
            continue
        if 'Unity.exe' not in files:
            continue
        dirs[:] = []
        editor_dirs.append(str(root_path.parent))

    return editor_dirs


def __get_version_darwin(app: str) -> UnityVersion:
    version = 0, 0, 0, 0
    version_str = str()

    def log_func(line: str):
        nonlocal version_str
        if line.startswith(': kMDItemVersion'):
            version_str = line.rstrip()

    try:
        return_code = run_process(['mdls', app], log_func=log_func)
        if return_code == 0 and version_str:
            regex_match = match(':\\s*kMDItemVersion\\s*=\\s*"Unity version (\\d+).(\\d+).(\\d+)f(\\d+)"', version_str)
            version = tuple(map(int, regex_match.groups()))
    except Exception:
        version = __match_version_string(app)
    if version == (0, 0, 0, 0):
        version = __match_version_string(app)

    return UnityVersion(*version)


def __get_version_linux(app: str) -> UnityVersion:
    version = __match_version_string(app)
    return UnityVersion(*version)


def __get_version_windows(app: str) -> UnityVersion:
    line_num = 1
    version = 0, 0, 0, 0
    version_str = str()

    def log_func(line: str):
        nonlocal line_num
        nonlocal version_str
        if line_num == 4:
            version_str = line.rstrip()
        line_num += 1

    app = app.replace('\\', '\\\\')

    try:
        return_code = run_process(['wmic', 'datafile', 'where', f'Name="{app}"', 'get', 'Version'], log_func=log_func)
        if return_code == 0 and version_str:
            regex_match = match(': (\\d+).(\\d+).(\\d+).(\\d+)', version_str)
            version = tuple(map(int, regex_match.groups()))
    except Exception:
        version = __match_version_string(app)
    if version == (0, 0, 0, 0):
        version = __match_version_string(app)

    return UnityVersion(*version)


def __match_version_string(app: str) -> Tuple[int, int, int, int]:
    version = 0, 0, 0, 0

    regex_match = match('.*(?:/|\\\)(\\d+).(\\d+).(\\d+)f(\\d+)(?:/|\\\?)', app)
    if regex_match is not None:
        version = tuple(map(int, regex_match.groups()))

    return version


unity_platform = {
    'Darwin': {
        'app': 'Unity.app',
        'exec': 'Unity.app/Contents/MacOS/Unity',
        'data': 'Unity.app/Contents',
        'libcache': [
            'Unity.app/Contents/Managed/UnityEngine',
            'Unity.app/Contents/Resources/PackageManager/ProjectTemplates/libcache',
        ],
        'mono_bin': 'Unity.app/Contents/MonoBleedingEdge/bin',
        'mcs': 'Unity.app/Contents/MonoBleedingEdge/bin/mcs',
        'find': (__find_darwin, ['/Applications']),
        'get_version': __get_version_darwin
    },
    'Linux': {
        'app': 'Editor/Unity',
        'exec': 'Editor/Unity',
        'data': 'Editor/Data',
        'libcache': [
            'Editor/Data/Managed/UnityEngine',
            'Editor/Data/Resources/PackageManager/ProjectTemplates/libcache',
        ],
        'mono_bin': 'Editor/Data/MonoBleedingEdge/bin',
        'mcs': 'Editor/Data/MonoBleedingEdge/bin/mcs',
        'find': (__find_linux, ['/opt']),
        'get_version': __get_version_linux
    },
    'Windows': {
        'app': 'Editor/Unity.exe',
        'exec': 'Editor/Unity.exe',
        'data': 'Editor/Data',
        'libcache': [
            'Editor/Data/Managed/UnityEngine',
            'Editor/Data/Resources/PackageManager/ProjectTemplates/libcache',
        ],
        'mono_bin': 'Editor/Data/MonoBleedingEdge/bin',
        'mcs': 'Editor/Data/MonoBleedingEdge/bin/mcs.bat',
        'find': (__find_windows, ['C:/Program Files', 'C:/Program Files (x86)']),
        'get_version': __get_version_windows
    },
}


class UnityEditor(object):

    path: Path
    exec: Path
    mcs: Path
    version: UnityVersion

    def __init__(self, editor_dir: str):
        sys = system()
        self.path = Path(editor_dir)
        self.exec = self.path / unity_platform[sys]['exec']
        self.mcs = self.path / unity_platform[sys]['mcs']
        self.version = unity_platform[sys]['get_version'](str(self.path / unity_platform[sys]['app']))

        if not self.exec.exists():
            raise Exception('Executable not found')

    def __repr__(self):
        return str(self.path)

    @staticmethod
    def find_all(*args: str) -> List[UnityEditor]:
        sys = system()
        if sys not in unity_platform.keys():
            raise NotImplementedError
        func, dirs = unity_platform[sys]['find']
        search_dirs = []
        search_dirs.extend(dirs if len(args) == 0 else
                           list(filter(lambda p: Path(p).is_dir(), args)))
        editor_dirs = []
        for d in search_dirs:
            editor_dirs.extend(func(d))
        editors = [UnityEditor(e) for e in editor_dirs]

        return editors

    @staticmethod
    def find_in(*args: str,
                cache: str = None) -> List[UnityEditor]:
        if cache is not None:
            cache_path = Path(cache)
            if cache_path.exists():
                editor_dirs = loads(cache_path.read_text())
                return [UnityEditor(e) for e in editor_dirs]
            else:
                editors = UnityEditor.find_all(*args)
                editor_dirs = [str(e) for e in editors]
                cache_path.touch()
                cache_path.write_text(dumps(editor_dirs, indent=2))
                return editors
        else:
            return UnityEditor.find_all(*args)

    @staticmethod
    def find_libcache(editor: UnityEditor) -> List[str]:
        return [str(editor.path / d) for d in unity_platform[system()]['libcache']]

    @staticmethod
    def find_libs(editor: UnityEditor) -> List[str]:
        libs = {}
        for d in editor.get_libcache():
            libcache_path = Path(d)
            for root, _, files in walk(str(libcache_path)):
                root_path = Path(root)
                for f in files:
                    file_path = Path(f)
                    if not '.dll' == file_path.suffix:
                        continue
                    file_name = str(file_path.name)
                    if file_name in libs.keys():
                        continue
                    libs[file_name] = str(root_path / file_path)

        return list(libs.values())

    def compile(self, *args: str,
                defines: List[str] = None,
                debug: bool = False,
                doc: str = None,
                nostdlib: bool = False,
                nowarn: List[str] = None,
                optimize: bool = False,
                out: str = None,
                references: List[str] = None,
                stacktrace: bool = False,
                target: str = None,
                unsafe: bool = False,
                warnaserror: List[str] = None,
                log_func: Callable[[str], None] = None) -> int:
        cwd_path = Path(getcwd())
        tmp_path = cwd_path / f'tmp-{datetime.now().strftime("%Y%m%d%H%M%S")}'
        tmp_path.mkdir()
        command = [str(self.mcs)]
        if defines is not None:
            command.append(f'-d:{";".join(defines)}')
        if debug:
            command.append('-debug')
        if doc is not None:
            command.append(f'-doc:{doc}')
        if nostdlib:
            command.append('-nostdlib')
        if nowarn is not None:
            command.append(f'-nowarn:{",".join(nowarn)}')
        if optimize:
            command.append('-optimize')
        if out is not None:
            command.append(f'-out:{out}')
        refs = []
        for r in references if references is not None else []:
            r_path = Path(r)
            if r_path.exists():
                r_name = r_path.name
                copyfile(str(r_path), str(tmp_path / r_name))
                refs.append(r_name)
        if len(refs) > 0:
            command.append(f'-r:{",".join(refs)}')
        if stacktrace:
            command.append('--stacktrace')
        if target is not None and target in ['exe', 'library', 'module', 'winexe']:
            command.append(f'-t:{target}')
        if unsafe:
            command.append('-unsafe')
        if warnaserror is not None:
            command.append(f'-warnaserror:{",".join(warnaserror)}')
        for f in args:
            f_path = Path(f)
            if f_path.exists():
                f_name = f_path.name
                copyfile(str(f_path), str(tmp_path / f_name))
        command.append('*.cs')
        try:
            chdir(str(tmp_path))
            return_code = run_process(command, log_func=log_func)
            if return_code == 0:
                if out is not None:
                    out_path = tmp_path / out
                    if out_path.exists():
                        move(str(out_path), str(cwd_path / out))
                if doc is not None:
                    doc_path = tmp_path / doc
                    if doc_path.exists():
                        move(str(doc_path), str(cwd_path / doc))
        finally:
            chdir(str(cwd_path))
            rmtree(str(tmp_path), ignore_errors=True)

        return return_code

    def get_libcache(self) -> List[str]:
        return UnityEditor.find_libcache(self)

    def get_libs(self) -> List[str]:
        return UnityEditor.find_libs(self)

    def run(self, *args: str,
            cli: bool = True,
            log_func: Callable[[str], None] = None) -> int:
        command = [str(self.exec)]
        command.extend(args)
        if cli:
            for o in ['-batchmode', '-nographics', '-quit', '-silent-crashes']:
                if o not in command:
                    command.append(o)

        return run_process(command, log_func=log_func)
