install:
	blender -b -P enableaddon.py

watch_log: install
	echo "" > /tmp/blender-stats.log && tail -f /tmp/blender-stats.log

.PHONY: install
