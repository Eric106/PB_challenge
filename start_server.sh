#!/bin/bash
ssl_cert="src/ssl_data/playbusiness.test.crt"
ssl_key="src/ssl_data/playbusiness.test.key"

workdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

startup="gunicorn -w=$(python set_workers.py) --certfile $ssl_cert --keyfile $ssl_key -b 0.0.0.0:65443 startup:app"

tmux new-session -d -s back_end
tmux send-keys -t back_end.0 "cd $workdir " ENTER
tmux send-keys -t back_end.0 "conda activate back_end " ENTER
tmux send-keys -t back_end.0 "$startup " ENTER
