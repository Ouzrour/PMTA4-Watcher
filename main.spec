# -*- mode: python -*-

block_cipher = None


a = Analysis(['application.py'],
             pathex=['E:\\mailing\\3. PMTA Watcher'],
             binaries=[],
             datas=[('icon.ico', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('header.png','E:\\mailing\\3. PMTA Watcher\\header.png', "DATA")]
a.datas += [('icon.png','E:\\mailing\\3. PMTA Watcher\\icon.png', "DATA")]
a.datas += [('beep.mp3','E:\\mailing\\3. PMTA Watcher\\beep.mp3', "DATA")]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Header Parser By.Ouzrour',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='icon.ico')