import argparse
import datetime
import json
from pathlib import Path

from pydantic import BaseModel


class Keymap(BaseModel):
    """キーコード"""

    full_screenshot: int
    mouse_screenshot: int
    back: int
    forward: int
    exit: int


class Config(BaseModel):
    """設定"""

    play_sound: bool
    keymap: Keymap


def load_config(json_path: Path | None = None) -> Config:
    """jsonを読み込んでConfigにする"""
    if json_path is None:
        json_path = Path(__file__).parent.parent / Path("config.json")
    with open(json_path, "r") as f:
        config = json.load(f)
    return Config(**config)


def get_numbers(dirname: str) -> list[int]:
    """
    指定されたディレクトリが含む子ディレクトリ一覧を返す。
    子ディレクトリの名前はすべて整数でなければならない。
    子ディレクトリは一つ以上なければならない。
    そうでなければ例外を送出する。

    Args:
        dirname: ディレクトリ名

    Returns:
        子ディレクトリ名一覧
    """
    parent = Path(dirname)

    if not parent.exists():
        raise Exception("ディレクトリが存在しません。")

    try:
        children = sorted(
            [int(child.name) for child in parent.glob("*") if child.is_dir()]
        )
    except:
        raise Exception("子ディレクトリの名前は整数でなければいけません。")

    if len(children) == 0:
        raise Exception("指定されたディレクトリが空です。")

    return children


def parse() -> tuple[list[int], int, str]:
    """
    引数をパースする

    Returns:
        項番一覧、初期項番、作成する親ディレクトリの名前
    """

    parser = argparse.ArgumentParser(description="スクリーンショットを連続で撮影する。")
    parser.add_argument(
        "-n",
        "--numbers",
        type=int,
        nargs="*",
        help="項番。スペース区切りの整数で指定。",
    )
    parser.add_argument(
        "-s", "--start", default=None, type=int, help="撮影開始時の項番。"
    )
    parser.add_argument("-d", "--dirname", type=str, help="保存先のディレクトリ名。")

    args = parser.parse_args()
    numbers, start, dirname = args.numbers, args.start, args.dirname

    if (numbers is None) and (dirname is None):
        raise Exception("項番とディレクトリ名がいずれも指定されていません。")
    elif numbers is None:
        numbers = get_numbers(dirname)
    elif dirname is None:
        dirname = datetime.datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )  # デフォルトの保存先ディレクトリ

    try:
        dir_idx = numbers.index(start)
    except:
        dir_idx = 0

    return numbers, dir_idx, dirname


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

    parent = Path(dirname)
    children = [parent / Path(f"{n}") for n in numbers]
    parent.mkdir(exist_ok=True, parents=True)
    for child in children:
        child.mkdir(exist_ok=True)
    return children
