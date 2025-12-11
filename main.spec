from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path
from PyInstaller.utils.hooks import collect_all
import os

# -*- mode: python ; coding: utf-8 -*-

# --- COLLECT KIVYMD DATA ---
# This ensures all KivyMD assets, modules, and dependencies are included
kivymd_datas, kivymd_binaries, kivymd_hiddenimports = collect_all('kivymd')

# --- DEFINE ASSETS ---
# Include all KV files and asset folders
# Format: (Source Path, Destination Path)
added_files = [
    ('Main/', 'Main/'),
    ('assets/', 'assets/'),
    ('user_data.db', '.'),
]

# Merge our assets with KivyMD's
all_datas = added_files + kivymd_datas
all_hiddenimports = [
    'sqlite3',
    'kivymd.icon_definitions', 
] + kivymd_hiddenimports

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=kivymd_binaries,
    datas=all_datas,
    hiddenimports=all_hiddenimports,
    hookspath=[kivymd_hooks_path],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='OctaTechApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OctaTechApp',
)
