CURRENT_DIR = $(shell pwd)

export CURRENT_DIR
setup:
	redis-cli -n 5 FLUSHALL
	rm -rf $$CURRENT_DIR/logs/ && \
	mkdir -p $$CURRENT_DIR/logs/ && \
	touch $$CURRENT_DIR/logs/debug.log && \
	touch $$CURRENT_DIR/logs/error.log

scan:
	python mgallery.py -s

compare:
	python mgallery.py -c

resort:
	python mgallery.py -r

check:
	black .
	flake8 .
