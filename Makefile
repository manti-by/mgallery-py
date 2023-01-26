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

export MIGRATION_SCRIPT
setup:
	sqlite3 db.sqlite "$$MIGRATION_SCRIPT" && \
	touch logs/debug.log && \
	touch logs/error.log

clean:
	rm -rf db.sqlite && \
	rm -rf logs/debug.log && \
	rm -rf logs/error.log

scan:
	python mgallery.py -s

report:
	python mgallery.py -r

compare:
	python mgallery.py -c

reload: clean setup scan report

check:
	black .
	flake8 .
