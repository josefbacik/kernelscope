#
# Based on offcputime from bcc by Brendan Gregg.

from bcc import BPF
from KernelscopeLogger import KernelscopeLogger
from time import sleep
import signal
import platform
import re
import socket


threshold = 5000
sleep_type = 2

duration = 60
debug = 0
maxdepth = 20    # and MAXDEPTH

# signal handler
def signal_ignore(signal, frame):
    print()

# define BPF program
bpf_text = """
#include <uapi/linux/ptrace.h>
#include <uapi/linux/perf_event.h>
#include <linux/version.h>
#include <linux/sched.h>

struct key_t {
	char target[TASK_COMM_LEN];
        u32 pid;
	u32 tret;
};
BPF_HASH(counts, struct key_t);
BPF_HASH(start, u32);

BPF_HASH(wokeby, u32, struct wokeby_t);
BPF_STACK_TRACE(stackmap, 10000)

int oncpu(struct pt_regs *ctx, struct task_struct *p) {
    u32 pid = p->pid;
    u64 ts, *tsp;

    // record previous thread sleep time
    if (SLEEP_TYPE_FILTER) {
        ts = bpf_ktime_get_ns();
        start.update(&pid, &ts);
    }

    // calculate current thread's delta time
    pid = bpf_get_current_pid_tgid();
    tsp = start.lookup(&pid);
    if (tsp == 0)
        return 0;        // missed start or filtered
    u64 cur = bpf_ktime_get_ns();
    if (cur < *tsp)
        return 0;        // skip entries that go backwards
    u64 delta = bpf_ktime_get_ns() - *tsp;
    start.delete(&pid);
    delta = delta / 1000;
    if (delta < MINBLOCK_US)
        return 0;

    // create map key
    u64 zero = 0, *val;
    struct key_t key = {};

    bpf_get_current_comm(&key.target, sizeof(key.target));
    key.tret = stackmap.get_stackid(ctx, BPF_F_FAST_STACK_CMP);
    key.pid = pid;

    val = counts.lookup_or_init(&key, &zero);
    (*val) += delta;
    return 0;
}
"""
bpf_text = bpf_text.replace('MINBLOCK_US', str(threshold))
sleep_type_filter = '1'
if sleep_type > 0:
    sleep_type_filter = ('p->state == %d' % (sleep_type))
bpf_text = bpf_text.replace('SLEEP_TYPE_FILTER', sleep_type_filter)
if debug:
    print(bpf_text)

# initialize BPF
b = BPF(text=bpf_text)
b.attach_kprobe(event="finish_task_switch", fn_name="oncpu")
matched = b.num_open_kprobes()
if matched != 1:
    print("%d functions traced. Exiting." % (matched))
    exit()

logger = KernelscopeLogger("http://localhost:8080")
done = 0
# output
while (done == 0):
    try:
        sleep(duration)
    except KeyboardInterrupt:
        # as cleanup can take many seconds, trap Ctrl-C:
        signal.signal(signal.SIGINT, signal_ignore)
        done = 1

    counts = b.get_table("counts")
    stacks = b.get_table("stackmap")
    for k, v in sorted(counts.items(), key=lambda counts: counts[1].value):
        # TODO convert to StackWalker next time somebody updates bcc-py
        try:
            sleeper = stacks[stacks.Key(k.tret)]
        except:
            continue
        sleep_trace = []
        wake_trace = []
        # print default multi-line stack output
        for i in range(0, maxdepth):
            if sleeper.ip[i] == 0:
                break
            sleep_trace.append(b.ksym(sleeper.ip[i]))
        data = {
            'process': str(k.target),
            'pid': int(k.pid),
            'elapsed': v.value,
            'stack': ";".join(sleep_trace),
        }
        logger.add_entry(data)
    logger.submit()
    counts.clear()
    stacks.clear()
exit()
