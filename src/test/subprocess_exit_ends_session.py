import re

from util import *

BAD_TOKEN = r'EXIT-SUCCESS'
GOOD_TOKEN = r'Inferior 1 \(process \d+\) exited normally'

def observe_child_crash_and_exit():
    expect_gdb('Program received signal SIGSEGV')

    send_gdb('c')
    for line in iterlines_both():
        if m := re.search(BAD_TOKEN, line):
            failed(f'Saw illegal token "{BAD_TOKEN}"')
        if m := re.search(GOOD_TOKEN, line):
            return

send_gdb('c')
observe_child_crash_and_exit()

restart_replay()
observe_child_crash_and_exit()

ok()
