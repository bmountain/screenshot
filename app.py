from pywinauto.win32_hooks import Hook
from make_dirs import MakeDirs
from screenshot import ScreenShot
from pathlib import Path
import sys, time

try:
    workdir = Path.cwd()
    dir_maker = MakeDirs(workdir)
    dirs = dir_maker.make_dirs()
    hk = Hook()
    ss = ScreenShot(dirs=dirs)
    hk.handler = ss.on_event
    time.sleep(1)
    hk.hook(keyboard=True, mouse=True)
except:
    print("pywinauto終了")
    sys.exit()
