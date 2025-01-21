from src import parse
from src.screenshot_class import start_app

number, start, dirname = parse.parse()
dirs = parse.makedirs(number, dirname)
start = start if start >= 1 else min(number)
start_app(dirs, number.index(start))
