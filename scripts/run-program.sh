#!/usr/bin/env bash
script="$1"
ssh pi@testpi.local "sudo python Projects/sensorkit/scripts/python/${script}.py flask run"
