#!/bin/bash
eval $(ps -ef | grep "[0-9] python tcp-multiplexer\\.py" | awk '{print "kill "$2}')
python tcp-multiplexer.py