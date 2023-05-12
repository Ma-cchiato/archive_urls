import sys
from PyInstaller.__main__ import run

if __name__ == '__main__':
    opts = ['archive_urls.py', '-F', '--console']
    run(opts)
