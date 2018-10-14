uwsgi : nohup uwsgi --socket 127.0.0.1:8000 -w runserver:app &
flask_sockets local : gunicorn -w 4 -b 127.0.0.1:8000 -k flask_sockets.worker --reload runserver:app

server0 : gunicorn --worker-class eventlet -w 1 runserver:app -u root -g apache --threads 4 --keep-alive 10
server1 : gunicorn --worker-class eventlet -w 1 -b 127.0.0.1:8001 runserver:app -u root -g apache --threads 4 --keep-alive 10
dev : gunicorn --worker-class eventlet -w 1 -b 127.0.0.1:9001 runserver:app -u root -g apache --threads 4 --keep-alive 10

flask_sockets remote :nohup gunicorn -w 4 -b 0.0.0.0:8000 -k flask_sockets.worker --reload runserver:app -u root -g apache &
