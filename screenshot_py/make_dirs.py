from pathlib import Path
import glob, os, sys


class MakeDirs:
    """テキストファイルに書かれたディレクトリ一覧からディレクトリを生成するプロンプト"""

    def __init__(self, workdir):
        self.workdir = Path(workdir)
        self.text_files = None
        self.dirs = None
        self.dir_idx = None
        self.set_params()

    def set_params(self):
        """ワーキングディレクトリを検証しworkdirとtext_filesをセット"""
        try:
            os.chdir(self.workdir)
        except:
            print("ディレクトリが見つかりませんでした")
            sys.exit()
        self.text_files = glob.glob("*.txt")
        if len(self.text_files) == 0:
            print("テキストファイルがありません")
            sys.exit()

    def choose_file(self):
        """ユーザにテキストファイルを選択してもらう
        選択されたファイルに書かれたディレクトリを生成しクラス変数にセットする
        """
        while True:
            print(f"保存先ディレクトリ: {self.workdir}")
            print("テキストファイルを選択してください (q: 終了):")
            for i, file in enumerate(self.text_files):
                print(f"{i}: {file}")
            response = input()
            if response == "q":
                print("終了します")
                sys.exit()
            try:
                response = int(response)
                if response >= 0 and response < len(self.text_files):
                    break
                else:
                    print("無効な選択です")
            except:
                print("無効な選択です")

        dir_list_file = self.workdir / Path(self.text_files[response])
        with open(dir_list_file, "r") as file:
            dir_names = [line.strip() for line in file]
        dirs = [self.workdir / Path(dir_name) for dir_name in dir_names]

        print("以下のディレクトリを作成します")
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
        self.dirs = dirs

    def choose_starting_dir(self):
        """スクショ収集を開始するディレクトリを選択してもらう"""
        while True:
            print(
                "スクショ取得を開始するディレクトリを選択してください (Enter: 0を選択)"
            )
            for i, dir in enumerate(self.dirs):
                print(f"{i}: {dir}")
            response = input()
            if len(response) == 0:
                self.dir_idx = 0
                break
            try:
                response = int(response)
                if response >= 0 and response < len(self.dirs):
                    self.dir_idx = response
                    break
                else:
                    print("無効な選択です")
            except:
                print("無効な選択です")

    def out(self):
        return self.dirs, self.dir_idx


def make_dirs(workdir):
    dirmaker = MakeDirs(workdir)
    dirmaker.set_params()
    dirmaker.choose_file()
    dirmaker.choose_starting_dir()
    return dirmaker.out()


if __name__ == "__main__":
    workdir = Path.cwd()
    test = MakeDirs(workdir)
    test.make_dirs()
