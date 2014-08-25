from os import environ
from os.path import dirname
import sys

print("BYE")

def hi():
    print("BYE")

def set_django_env():
    sys.path.append(dirname(dirname(__file__)))
    environ.setdefault("DJANGO_SETTINGS_MODULE", "eos.settings")

if __name__ == '__main__':
    raise Exception('directly running this file is useless')