#!/usr/bin/env bash
script="$1"
ssh pi@testpi.local "sudo lsof -t -i tcp:8888 | sudo kill -9 && sudo python Projects/sensorkit/scripts/python/${script}.py"
