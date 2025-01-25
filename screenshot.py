from src.screenshot_app import start_app
from src.screenshot_utils import load_config, makedirs, parse

number, dir_idx, dirname = parse()
config = load_config()
dirs = makedirs(number, dirname)
start_app(dirs, dir_idx, config)
