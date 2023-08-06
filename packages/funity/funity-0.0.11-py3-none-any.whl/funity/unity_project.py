#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import walk
from pathlib import Path
from shutil import rmtree
from typing import List, Optional

from yaml import FullLoader, load


class UnityProject(object):
    SPECIAL_DIRS = ['Editor', 'Gizmos', 'Plugins', 'Resources', 'Standard Assets', 'StreamingAssets']

    path: Path

    def __init__(self, project_dir: str):
        self.path = Path(project_dir)

    def __repr__(self):
        return str(self.path)

    @staticmethod
    def __load_unity_yaml_file(path: Path):
        text = str()
        try:
            with path.open(encoding='UTF-8') as file:
                for line in file:
                    text += f'--- {line.split(" ")[2]}\n' if line.startswith('--- !u!') else line
            return load(text, Loader=FullLoader)

        except UnicodeDecodeError:
            return load('data:', Loader=FullLoader)

    def __get_editor_build_settings(self):
        editor_build_settings_path = self.get_project_settings_path() / 'EditorBuildSettings.asset'
        if not editor_build_settings_path.exists():
            return None
        yaml_object = UnityProject.__load_unity_yaml_file(editor_build_settings_path)
        if 'EditorBuildSettings' not in yaml_object:
            return None
        editor_build_settings = yaml_object['EditorBuildSettings']

        return editor_build_settings

    def __get_input_manager(self):
        input_manager_path = self.get_project_settings_path() / 'InputManager.asset'
        if not input_manager_path.exists():
            return None
        yaml_object = UnityProject.__load_unity_yaml_file(input_manager_path)
        if 'InputManager' not in yaml_object:
            return None
        input_manager = yaml_object['InputManager']

        return input_manager

    def __get_player_settings(self):
        project_settings_path = self.get_project_settings_path() / 'ProjectSettings.asset'
        if not project_settings_path.exists():
            return None
        yaml_object = UnityProject.__load_unity_yaml_file(project_settings_path)
        if 'PlayerSettings' not in yaml_object:
            return None
        player_settings = yaml_object['PlayerSettings']

        return player_settings

    def __get_tag_manager(self):
        tag_manager_path = self.get_project_settings_path() / 'TagManager.asset'
        if not tag_manager_path.exists():
            return None
        yaml_object = UnityProject.__load_unity_yaml_file(tag_manager_path)
        if 'TagManager' not in yaml_object:
            return None
        tag_manager = yaml_object['TagManager']

        return tag_manager

    def delete_asset(self,
                     asset: str) -> None:
        asset_path = self.get_assets_path() / asset
        if asset_path.exists():
            if asset_path.is_file():
                asset_path.unlink()
            elif asset_path.is_dir():
                rmtree(str(asset_path), ignore_errors=True)
        asset_meta_path = asset_path.with_suffix(str(asset_path.suffix) + '.meta')
        if asset_meta_path.exists() and asset_meta_path.is_file():
            asset_meta_path.unlink()

    def find_assets(self,
                    file_extensions: List[str] = None,
                    skip_folders: List[str] = None,
                    skip_dirs: List[str] = None) -> List[str]:
        file_extensions = file_extensions if file_extensions is not None else ['']
        file_extensions = [file_extension.casefold() for file_extension in file_extensions]
        file_exts = tuple(file_extensions)
        skip_folders = skip_folders if skip_folders is not None else []
        skip_dirs = [Path(d) for d in skip_dirs] if skip_dirs is not None else []
        asset_files = []
        for root, dirs, files in walk(str(self.get_assets_path())):
            rel_root_path = Path(root).relative_to(self.path)
            dirs[:] = [d for d in dirs if d not in skip_folders]
            if rel_root_path in skip_dirs:
                dirs[:] = []
                files[:] = []
            for f in files:
                if f.casefold().endswith(file_exts):
                    asset_files.append(str(rel_root_path / f))

        return asset_files

    def get_asset_meta(self,
                       asset: str) -> str:
        assets_path = self.get_assets_path()
        asset_path = assets_path / asset
        asset_meta_path = asset_path.with_suffix(str(asset_path.suffix) + '.meta')

        return str(asset_meta_path.relative_to(assets_path))

    def get_assets_path(self) -> Path:
        return self.path / 'Assets'

    def get_build_scenes(self):
        editor_build_settings = self.__get_editor_build_settings()
        if editor_build_settings is None or 'm_Scenes' not in editor_build_settings:
            return None
        scenes = editor_build_settings['m_Scenes']

        return [(s['path'], s['guid'], s['enabled'] > 0) for s in scenes]

    def get_editor_version(self) -> Optional[str]:
        project_version_path = self.get_project_settings_path() / 'ProjectVersion.txt'
        if not project_version_path.exists():
            return None
        yaml_object = UnityProject.__load_unity_yaml_file(project_version_path)

        return str(yaml_object['m_EditorVersion']) if 'm_EditorVersion' in yaml_object else None

    def get_player_settings_value(self, key: str):
        player_settings = self.__get_player_settings()
        if player_settings is None or key not in player_settings:
            return None

        return player_settings[key]

    def get_project_bundle_version(self) -> Optional[str]:
        return self.get_player_settings_value('bundleVersion')

    def get_project_company_name(self) -> Optional[str]:
        return self.get_player_settings_value('companyName')

    def get_project_input_axes(self):
        input_manager = self.__get_input_manager()
        if input_manager is None or 'm_Axes' not in input_manager:
            return None
        axes = input_manager['m_Axes']

        return axes

    def get_project_layers(self,
                           include_none: bool = False) -> Optional[List[str]]:
        tag_manager = self.__get_tag_manager()
        if tag_manager is None or 'layers' not in tag_manager:
            return None
        layers = tag_manager['layers']

        return [l for l in layers if l is not None or include_none]

    def get_project_product_name(self) -> Optional[str]:
        return self.get_player_settings_value('productName')

    def get_project_sorting_layers(self) -> Optional[List[str]]:
        tag_manager = self.__get_tag_manager()
        if tag_manager is None or 'm_SortingLayers' not in tag_manager:
            return None
        sorting_layers = tag_manager['m_SortingLayers']

        return [s['name'] for s in sorting_layers]

    def get_project_tags(self) -> Optional[List[str]]:
        tag_manager = self.__get_tag_manager()
        if tag_manager is None or 'tags' not in tag_manager:
            return None
        tags = tag_manager['tags']

        return tags

    def get_project_settings_path(self) -> Path:
        return self.path / 'ProjectSettings'
