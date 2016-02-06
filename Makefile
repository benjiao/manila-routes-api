install: logs venv db

logs: 
    sudo mkdir -m 775 -p /var/log/dev
    sudo touch /var/log/dev/manila-routes-api.uwsgi.log
    sudo touch /var/log/dev/manila-routes-api.logi
    sudo chmod 775 /var/log/dev/manila-routes-api.uwsgi.log
    sudo chmod 775 /var/log/dev/manila-routes-api.uwsgi.logi

    sudo chown $(USER):$(USER) /var/log/dev/manila-routes-api.uwsgi.log
    sudo chown $(USER):$(USER) /var/log/dev/manila-routes-api.uwsgi.logi

venv: deps 
    virtualenv env
    env/bin/pip install -r setup/requirements.txt

db:
    env/bin/python load-routes.py

