#!/bin/bash
/usr/bin/python3 /mnt/led.py & # Code de détection
/usr/bin/python3 /mnt/log_script.py & # Code métier pour réaliser un POC
# A modifier si nouveau code métier.
wait