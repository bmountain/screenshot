from src import parse, screenshot

number, start, dirname = parse.parse()
dirs = parse.makedirs(number, dirname)
start = start if start >= 1 else min(number)
screenshot.start(dirs, number.index(start))
