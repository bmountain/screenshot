import argparse
import datetime
from pathlib import Path

DEBUG = True


def parse():
    """引数のパース"""
    if DEBUG:
        now = "test"
    else:
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    parser = argparse.ArgumentParser(description="スクリーンショットを連続で撮影する。")
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        nargs="*",
        required=True,
        help="項番。スペース区切りの自然数で指定。",
    )
    parser.add_argument(
        "-s", "--start", default=-1, type=int, help="撮影開始時の項番。"
    )
    parser.add_argument(
        "-d", "--dirname", default=now, type=str, help="保存先のディレクトリ名。"
    )
    args = parser.parse_args()
    return args.number, args.start, args.dirname


def makedirs(number, dirname):
    """引数からディレクトリを作成し保存先の子ディレクトリパスを返す"""
    parent = Path.cwd() / Path(dirname)
    children = [parent / Path(f"{n}") for n in number]
    parent.mkdir(exist_ok=True)
    for child in children:
        child.mkdir(exist_ok=True)
    return children


if __name__ == "__main__":
    number, start, dirname = parse()
    dirs = makedirs(number, dirname)
    start(dirs, number.index(start))
