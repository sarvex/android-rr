import collections
import sys
import re
from util import *

arch = get_exe_arch()

ArchInfo = collections.namedtuple('ArchInfo', ['ip_name'])
regex_info = {
    'i386': ArchInfo('eip'),
    'i386:x86-64': ArchInfo('rip'),
    'aarch64': ArchInfo('pc'),
}

syscall_re = re.compile("`SYSCALL: <unknown-syscall--1>' \\(state:EXITING_SYSCALL\\)")
sched_re = re.compile("`SCHED'")
eip_re = re.compile(f"{regex_info[arch].ip_name}:(0x[a-f0-9]+)")

sched_enabled = False
eip_enabled = False
eip = None
while True:
    line = sys.stdin.readline()
    if not line:
        break
    if syscall_re.search(line):
        sched_enabled = True
    if sched_enabled and sched_re.search(line):
        eip_enabled = True
    if eip_enabled:
        if m := eip_re.search(line):
            eip = m[1]
            break

if eip is None:
    failed(f'{regex_info[arch].ip_name} not found')

# The SCHED after getgid may land in libc, which might not be loaded yet, in
# which case setting a breakpoint there will cause gdb to barf. So run to
# 'main' at which point libc is definitely loaded.
send_gdb('b main')
expect_gdb('Breakpoint 1')
send_gdb('c')
expect_gdb('Breakpoint 1')

send_gdb(f'b *{eip}')
expect_gdb('Breakpoint 2')
send_gdb('c')
expect_gdb('Breakpoint 2')
expect_gdb('(rr)')

if arch == 'aarch64':
    send_gdb('p/x *(uint32_t*)$pc')
    expect_gdb('0x([a-f0-9]+)')
    if last_match().group(1) == 'd4200000':
        failed('saw breakpoint at current instruction')
elif arch in ['i386', 'i386:x86-64']:
    send_gdb('p/x *(char*)$pc')
    expect_gdb('0x([a-f0-9]+)')
    if last_match().group(1) == 'cc':
        failed('saw breakpoint at current instruction')
else:
    failed('Add check for this architecture')

ok()
