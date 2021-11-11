CURRENT_DIR = $(shell pwd)

define MIGRATION_SCRIPT
CREATE TABLE IF NOT EXISTS image (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT,
    name TEXT,
    phash TEXT,
    size INTEGER,
    width INTEGER,
    height INTEGER,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_image_path ON image (path);
CREATE INDEX idx_image_phash ON image (phash);
endef

export CURRENT_DIR
export MIGRATION_SCRIPT
setup:
	sqlite3 $$CURRENT_DIR/db.sqlite "$$MIGRATION_SCRIPT" && \
	mkdir -p $$CURRENT_DIR/logs/ && \
	touch $$CURRENT_DIR/logs/debug.log && \
	touch $$CURRENT_DIR/logs/error.log

export CURRENT_DIR
clean:
	rm -rf $$CURRENT_DIR/db.sqlite && \
	rm -rf $$CURRENT_DIR/logs/

scan:
	python mgallery.py -s

report:
	python mgallery.py -r

compare:
	python mgallery.py -c

reload: clean setup scan

check:
	black .
	flake8 .
