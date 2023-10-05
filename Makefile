flush-db:
	redis-cli -n 5 FLUSHALL

make-dirs:
	sudo mkdir -p /var/mgallery/thumbnails && \
	sudo chown manti:manti /var/mgallery/thumbnails

setup: flush-db make-dirs

dump:
	python mgallery.py -d

scan:
	python mgallery.py -s

compare:
	python mgallery.py -c

rename:
	python mgallery.py -r

resort:
	python mgallery.py -o

thumbnails:
	python mgallery.py -t

check:
	black .
	flake8 .

update-requirements:
	pcu requirements.txt -u