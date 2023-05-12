from util import *

gdb_signals = [
  '',
  'SIGHUP',
  'SIGINT',
  'SIGQUIT',
  'SIGILL',
  'SIGTRAP',
  'SIGABRT',
  'SIGBUS',
  'SIGFPE',
  '#SIGKILL',
  'SIGUSR1',
  'SIGSEGV',
  'SIGUSR2',
  'SIGPIPE',
  'SIGALRM',
  'SIGTERM',
  '#SIGSTKFLT',
  'SIGCHLD',
  'SIGCONT',
  '#SIGSTOP',
  'SIGTSTP',
  'SIGTTIN',
  'SIGTTOU',
  'SIGURG',
  'SIGXCPU',
  'SIGXFSZ',
  'SIGVTALRM',
  'SIGPROF',
  'SIGWINCH',
  'SIGIO',
  '#SIGPWR',
  'SIGSYS']

gdb_signals.extend('SIG%d'%sig for sig in range(32,65))
for sig in range(1,65):
    gdb_sig = gdb_signals[sig]
    if not gdb_sig.startswith('#'):
        send_gdb(f'handle {gdb_sig} stop')
        if gdb_sig in ['SIGINT', 'SIGTRAP']:
            expect_gdb('used by the debugger')
            send_gdb('y')
        expect_gdb('(rr)')
        send_gdb('c')
        expect_gdb(f'received signal {gdb_sig}')

ok()
