#!/bin/bash

.DEFAULT_GOAL := install

MOTION_VERSION := 4.4.0

install: \
	update_crontab \
	update_motion \
	restart_motion \
	monitor_motion \

# Add command removing old command preventing duplicates
# Remove each line with [PEEPHOLE] and 1 lines after (the cmd)
# After it cleans the blank lines (where >=2 appear)

.PHONY: update_crontab

update_crontab:
	@ ( \
		sudo crontab -l \
		| sed "/[PEEPHOLE]/, +1 d" \
		| awk '!NF {if (++n < 2) print; next}; {n=0; print}'; \
		cat cfg/cron/crontab \
	) | sudo crontab -
	sudo crontab -l
	@ echo

update_motion:
	@ echo "Updating script permissions..."
	@ chmod +x bin/*
	@ echo "Motion $(MOTION_VERSION) conf diff (< old | new >)..."
	@ colordiff "/etc/motion/motion-$(MOTION_VERSION).conf" "cfg/motion/motion-$(MOTION_VERSION).conf" || true
	@ echo "Setting motion config..."
	@ sudo cp -f "cfg/motion/motion-$(MOTION_VERSION).conf" "/etc/motion/motion-$(MOTION_VERSION).conf"
	@ sudo ln -sf "/etc/motion/motion-$(MOTION_VERSION).conf" "/etc/motion/motion.conf"
	@ echo "(Re)enable motion daemon..."
	@ sudo sed -i "s/start_motion_daemon=.*/start_motion_daemon=yes/" "/etc/default/motion"
	@ echo "(Re)create motion lib..."
	@ sudo -u motion mkdir -p "/var/lib/motion"
	@ sudo chown motion.motion "/var/lib/motion"
	@ sudo chmod a+rwxt "/var/run/motion"
	@ sudo mkdir -p "/var/log/peepcam/"
	@ sudo chmod 777 "/var/log/peepcam/"
	@ echo "(Re)create local symlinks"
	@ ln -sf "/var/lib/motion" "./lib"
	@ ln -sf "/var/log/peepcam" "./log"

restart_motion:
	@ echo "Restarting motion..."
	@ sudo systemctl restart motion

monitor_motion:
	@ sudo journalctl -fu motion

#=======================================

# These are my own targets

user = lheck
host = falcon.lan

sync: \
	sync_peepcam \
	install

# Update Makefile
sync_makefile:
	@ echo "Remote sync Makefile..."
	@ rsync -avh $(user)@$(host):'/home/$(user)/Dropbox/peephole-raspi/code/Makefile' "/home/$(user)/peepcam/"

# Update peepcam files
sync_peepcam:
	@ echo "Remote sync..."
	rsync -avh $(user)@$(host):'/home/$(user)/Dropbox/peephole-raspi/code/' "/home/$(user)/peepcam/" --delete

test_telegram:
	@ ./bin/send-to-telegram.py -n "_Testing Telegram routines..._"
	@ ./bin/send-to-telegram.py
	@ ./bin/send-to-telegram.py -p "./cfg/telegram/fdoor_bot.jpg"
	@ ./bin/send-to-telegram.py -v "./cfg/telegram/sample_640x360.mkv"
