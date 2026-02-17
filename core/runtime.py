import os
import sys

def restart_application():
    os.execl(sys.executable, sys.executable, *sys.argv)