#!bin/sh

flask db upgrade

exerc gunicorn --bind 0.0.0.0:80 "app:create_app()"