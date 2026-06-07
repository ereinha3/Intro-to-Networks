#!/usr/bin/env bash

set -euo pipefail

trap 'echo "Stopping routers..."; pkill -P $$ || true' EXIT

source "$(dirname "$0")/routers.env"
if [ -f "code/.venv/bin/activate" ]; then
  source code/.venv/bin/activate
fi

mkdir -p code
mkdir -p logs

PYTHONUNBUFFERED=1 python3 -m code.router6 | tee logs/router6.log &
PYTHONUNBUFFERED=1 python3 -m code.router5 | tee logs/router5.log &
PYTHONUNBUFFERED=1 python3 -m code.router4 | tee logs/router4.log &
PYTHONUNBUFFERED=1 python3 -m code.router3 | tee logs/router3.log &
PYTHONUNBUFFERED=1 python3 -m code.router2 | tee logs/router2.log &
PYTHONUNBUFFERED=1 python3 -m code.router1 | tee logs/router1.log &

wait
