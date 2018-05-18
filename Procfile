main_uwsgi : nohup uwsgi --socket 127.0.0.1:8080 -w runserver:app &
redis_web_socket : nohup gunicorn -w 1 -b 127.0.0.1:8080 -k flask_sockets.worker runserver:app &
