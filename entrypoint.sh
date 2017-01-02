#!/bin/bash
set -e
mount -t debugfs none /sys/kernel/debug/
exec "$@"
