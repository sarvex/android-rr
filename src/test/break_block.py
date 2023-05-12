from util import *

send_gdb('b breakpoint')
expect_gdb('Breakpoint 1')

for _ in range(2):
    send_gdb('c')
    expect_gdb('Breakpoint 1, breakpoint')

ok()
