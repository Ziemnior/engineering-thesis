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
    config.set('overtime', 'enable', 'true')
    config.add_section('worktime')
    config.set('worktime', 'lower_boundary', '8')
    config.set('worktime', 'upper_boundary', '16')
    config.add_section('salary')
    config.set('salary', 'base_salary', '10')
    config.set('salary', 'extended_salary', '20')
    config.set('salary', 'currency', 'PLN')
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
    config.set('salary', 'base_salary', str(form.base_salary.data))
    config.set('salary', 'extended_salary', str(form.extended_salary.data))
    config.set('salary', 'currency', str(form.currency.data))
    save_config(config)


def read_overtime_status():
    check_config_file()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config.getboolean('overtime', 'enable')


def read_worktime_hours():
    check_config_file()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return [config.getint('worktime', 'lower_boundary'), config.getint('worktime', 'upper_boundary')]


def read_currency():
    check_config_file()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config.get('salary', 'currency')


def read_base_hour_rate():
    check_config_file()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config.get('salary', 'base_salary')


def read_extended_hour_rate():
    check_config_file()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config.get('salary', 'extended_salary')
