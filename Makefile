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
	sqlite3 /home/manti/www/mgallery/db.sqlite "$$MIGRATION_SCRIPT" && \
	touch /home/manti/www/mgallery/logs/debug.log && \
	touch /home/manti/www/mgallery/logs/error.log

clean:
	rm -rf /home/manti/www/mgallery/db.sqlite && \
	rm -rf /home/manti/www/mgallery/logs/debug.log && \
	rm -rf /home/manti/www/mgallery/logs/error.log

scan:
	python mgallery.py -s

restart: clean setup scan

report:
	python mgallery.py -r

check:
	black .
	flake8 .
