# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['FlangeSheet.py'],
    pathex=[],
    binaries=[],
    datas=[('Data', 'Data'), ('flangeWindow.py', '.'), ('flangeWindow.ui', '.'), ('img', 'img'), ('license.key', '.'), ('license.dat', '.'), ('img_source_rc.py', '.')],
    hiddenimports=['registration_generator', 'registration_key_validator', 'registration_key_generator', 'flangeWindow'],
    hookspath=[],
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
    a.binaries,
    a.datas,
    [],
    name='FlangeSheet',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['fla_256.ico'],
)
