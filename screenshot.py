from src import parse
from src.screenshot_app import start_app

number, start, dirname = parse.parse()
dir_idx = number.index(start)
dirs = parse.makedirs(number, dirname)
start_app(dirs, dir_idx)
