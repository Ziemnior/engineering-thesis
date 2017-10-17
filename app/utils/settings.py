import configparser
import os

CONFIG_FILE = "settings.ini"


def save_config(config):
    with open(CONFIG_FILE, 'w') as cfg:
        config.write(cfg)


def check_config_file():
    if not os.path.exists(CONFIG_FILE) or os.path.getsize(CONFIG_FILE) == 0:
        default_config()


def default_config():
    config = configparser.ConfigParser()
    config.add_section('overtime')
    config.set('overtime', 'enable', 'True')
    config.add_section('worktime')
    config.set('worktime', 'lower_boundary', '8')
    config.set('worktime', 'upper_boundary', '16')
    save_config(config)


def print_config():
    check_config_file()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return {s: dict(config.items(s)) for s in config.sections()}


def update_config(form):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    config.set('overtime', 'enable', str(form.enable_worktime.data))
    config.set('worktime', 'lower_boundary', str(form.lower_boundary.data))
    config.set('worktime', 'upper_boundary', str(form.upper_boundary.data))
    save_config(config)
