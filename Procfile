uwsgi : nohup uwsgi --socket 127.0.0.1:8080 -w runserver:app &
websocket localhost : gunicorn -w 4 -b 127.0.0.1:8000 -k flask_sockets.worker --reload runserver:app
websocket remote host :nohup gunicorn -w 4 -b 0.0.0.0:8000 -k flask_sockets.worker --reload runserver:app -u root -g apache &
