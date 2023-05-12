from util import *
import re

arch = get_exe_arch()

if arch == 'aarch64':
    send_gdb('p $v0.d.u')
    expect_gdb('{0, 0}')
elif arch in ['i386', 'i386:x86-64']:
    send_gdb('p $xmm0')
    expect_gdb('v4_float = {0, 0, 0, 0}')

ok()
