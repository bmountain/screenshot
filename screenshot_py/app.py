from pywinauto.win32_hooks import Hook
from make_dirs import make_dirs
from screenshot import ScreenShot
import sys, time


def main(workdir):
    """ディレクトリの作成・スクリーンショット撮影を行う各モジュールを制御"""
    dirs, dir_idx = make_dirs(workdir)
    ss = ScreenShot(dirs=dirs, dir_idx=dir_idx)
    hk = Hook()
    hk.handler = ss.on_event
    time.sleep(0.5)
    hk.hook(keyboard=True, mouse=True)


if __name__ == "__main__":
    main(sys.argv[1])
