import argparse
import datetime
from pathlib import Path

from screenshot_app import start_app


def parse() -> tuple[list[int], int, str]:
    """
    引数をパースする

    Returns:
        項番一覧、初期項番、作成する親ディレクトリの名前
    """
    now = datetime.datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )  # デフォルトの保存先ディレクトリ

    parser = argparse.ArgumentParser(description="スクリーンショットを連続で撮影する。")
    parser.add_argument(
        "-n",
        "--numbers",
        type=int,
        nargs="*",
        required=True,
        help="項番。スペース区切りの自然数で指定。",
    )
    parser.add_argument(
        "-s", "--start", default=None, type=int, help="撮影開始時の項番。"
    )
    parser.add_argument(
        "-d", "--dirname", default=now, type=str, help="保存先のディレクトリ名。"
    )

    args = parser.parse_args()
    numbers, start, dirname = args.numbers, args.start, args.dirname

    # startが有効な値でなければnumbersの最小値とする
    if start is None or start not in numbers:
        start = min(numbers)

    return numbers, start, dirname


def makedirs(numbers: list[int], dirname: str) -> list[Path]:
    """
    親ディレクトリとその子ディレクトリを作る。
    子ディレクトリのパスを返す。

    Args:
        numbers: 項番一覧
        dirname: 親ディレクトリ名

    Returns:
        子ディレクトリのパス一覧
    """

    parent = Path.cwd() / Path(dirname)
    children = [parent / Path(f"{n}") for n in numbers]
    parent.mkdir(exist_ok=True)
    for child in children:
        child.mkdir(exist_ok=True)
    return children


if __name__ == "__main__":
    numbers, start, dirname = parse()
    dir_idx = numbers.index(start)
    dirs = makedirs(numbers, dirname)
    start_app(dirs, dir_idx)
