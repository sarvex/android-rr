import sys
import re

syscall_re = re.compile("`SIGNAL: ")
time_re = re.compile("global_time:(\d+)")
futex_time = 999999999

while True:
    line = sys.stdin.readline()
    if not line:
        break
    if syscall_re.search(line):
        if m := time_re.search(line):
            futex_time = m[1]

print(futex_time)
