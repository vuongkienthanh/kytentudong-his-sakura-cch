# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

main= Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[("icon.ico", ".")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
main_pyz = PYZ(main.pure, main.zipped_data, cipher=block_cipher)
main_exe = EXE(
    main_pyz,
    main.scripts,
    [],
    exclude_binaries=True,
    name='main',
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
    icon=['icon.ico'],
)

coll = COLLECT(
    main_exe,
    main.binaries,
    main.zipfiles,
    main.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='kytentudong',
)