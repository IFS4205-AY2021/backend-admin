#! bin/bash

# ls /home
# ls /home/admin
export WORKDIR=$(pwd)
export $(grep -v '^#' .env | xargs)

python3 resources/wait_for_mysql.py

echo "Starting Django Server..."
python3 app/manage.py runserver 0.0.0.0:8000

unset $(grep -v '^#' .env | sed -E 's/(.*)=.*/\1/' | xargs)
# For container debug
sleep 600
