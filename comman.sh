[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/ubuntu/blazestore/Django_ecommerce
ExecStart=/home/ubuntu/blazestore/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/blazestore/Django_ecommerce.sock Django_ecommerce.wsgi:application

[Install]
WantedBy=multi-user.target













