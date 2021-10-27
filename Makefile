define MIGRATION_SCRIPT
CREATE TABLE IF NOT EXISTS gallery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT,
    name TEXT,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS image (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gallery_id INTEGER,
    path TEXT,
    name TEXT,
    phash TEXT,
    size INTEGER,
    width INTEGER,
    height INTEGER,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);
endef

export MIGRATION_SCRIPT
setup:
	sqlite3 /home/manti/www/mgallery/db.sqlite "$$MIGRATION_SCRIPT" && \
	touch /home/manti/www/mgallery/debug.log && \
	touch /home/manti/www/mgallery/error.log

clean:
	python mgallery.py -c && \
	rm -rf /home/manti/www/mgallery/db.sqlite && \
	rm -rf /home/manti/www/mgallery/debug.log && \
	rm -rf /home/manti/www/mgallery/error.log

worker:
	rq worker -c mgallery.settings

scan:
	python mgallery.py -s

find:
	python mgallery.py -f

check:
	black --target-version py38 .
	flake8 .
