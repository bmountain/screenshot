from pathlib import Path
import glob, os, sys
from string import ascii_lowercase


class MakeDirs:
    """テキストファイルに書かれたディレクトリ一覧からディレクトリを生成するプロンプト"""

    def __init__(self, workdir):
        try:
            self.workdir = Path(workdir)
            os.chdir(self.workdir)
        except:
            print("指定されたディレクトリが見つかりませんでした")
            sys.exit()
        self.text_files = glob.glob("*.txt")
        if len(self.text_files) > 26:
            print("テキストファイルが多すぎます")
            sys.exit()

    def make_dirs(self):
        alpha = list(ascii_lowercase)[: len(self.text_files)]
        while True:
            print(f"保存先ディレクトリ: {self.workdir}")
            print(
                "保存先ディレクトリ名一覧が各行に書かれたテキストファイルを選択してください:"
            )
            for c, file in zip(alpha, self.text_files):
                print(f"{c}: {file}")
            print("0: 終了")
            res_file = input()
            if res_file == "0":
                print("終了します")
                sys.exit()
            try:
                idx = alpha.index(res_file)
                break
            except:
                print("存在しない選択肢です")
        dir_list_file = self.workdir / Path(self.text_files[idx])
        with open(dir_list_file, "r") as file:
            dir_names = [line.strip() for line in file]
        dirs = [self.workdir / Path(dir_name) for dir_name in dir_names]
        print("以下のディレクトリを生成します")
        for dir in dirs:
            print(dir)
        print("OK? (y/n)")
        res_conf = input()
        if res_conf == "y":
            for dir in dirs:
                if not dir.exists():
                    dir.mkdir(parents=True)
        else:
            print("終了します")
            sys.exit()
        return dirs


if __name__ == "__main__":
    workdir = Path.cwd()
    # workdir = "hoge"
    test = MakeDirs(workdir)
    test.make_dirs()
