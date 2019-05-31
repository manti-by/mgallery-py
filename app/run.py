import os

role = os.getenv("ROLE")
if role == "app":
    os.system("python main.py -a")
elif role == "celery":
    os.system(
        "celery worker -A core --concurrency=4 -n worker@mgallery "
        "-f /var/log/mgallery/worker.log"
    )
elif role == "flower":
    os.system(
        "celery flower -A core --inspect_timeout=30000 --port=5505 "
        "--url_prefix=flower -f /var/log/mgallery/flower.log"
    )
else:
    print("OS env var ROLE -{}- not set".format(role))
    exit(-1)
