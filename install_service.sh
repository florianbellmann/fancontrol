#!/bin/bash
sudo cp fancontrol.service /lib/systemd/system/

sudo chmod 644 /lib/systemd/system/fancontrol.service
sudo systemctl daemon-reload
sudo systemctl enable fancontrol.service
sudo systemctl start fancontrol.service

sudo systemctl status fancontrol.service
