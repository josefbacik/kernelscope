from KernelscopeLogger import KernelscopeLogger

logger = KernelscopeLogger("http://localhost:8080")
foo = {}
foo["process"] = "fs_mark"
foo["pid"] = 1345
foo["stack"] = "write;btrfs_write;sleep"
foo["elapsed"] = 1234
logger.add_entry('offcputime', foo)
foo = foo.copy()
foo["process"] = "bar"
logger.add_entry('offcputime', foo)
logger.submit()
