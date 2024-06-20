#!/bin/bash

tmux send-keys -t back_end.0 C-c
tmux kill-session -t back_end