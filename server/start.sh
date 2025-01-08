#!/bin/bash

echo "Starting Backend"
cd "/mnt/c/Users/HHH/Desktop/files/New folder/mad_2_library/server"

# Activate virtual environment and store it in a variable
source newenv/bin/activate

# 1. Start Redis server  
xterm -e "source newenv/bin/activate && redis-server" &
echo $! > /tmp/redis.pid

# 2. Start MailHog
xterm -e "source newenv/bin/activate && MailHog" &
echo $! > /tmp/mailhog.pid

# 3. Start Flask application
xterm -e "source newenv/bin/activate && python app.py" &
echo $! > /tmp/flask.pid

# 4. Start Celery worker
xterm -e "source newenv/bin/activate && celery -A tasks.celery worker --loglevel=INFO" &
echo $! > /tmp/celery_worker.pid

# 5. Start Celery beat
xterm -e "source newenv/bin/activate && celery -A tasks.celery beat --loglevel=INFO" &
echo $! > /tmp/celery_beat.pid

echo "All services started"
