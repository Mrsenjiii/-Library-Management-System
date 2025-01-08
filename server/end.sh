#!/bin/bash

echo "Stopping Backend Services"

# Kill processes
if [ -f /tmp/redis.pid ]; then
  kill $(cat /tmp/redis.pid) && rm /tmp/redis.pid
fi

if [ -f /tmp/mailhog.pid ]; then
  kill $(cat /tmp/mailhog.pid) && rm /tmp/mailhog.pid
fi

if [ -f /tmp/flask.pid ]; then
  kill $(cat /tmp/flask.pid) && rm /tmp/flask.pid
fi

if [ -f /tmp/celery_worker.pid ]; then
  kill $(cat /tmp/celery_worker.pid) && rm /tmp/celery_worker.pid
fi

if [ -f /tmp/celery_beat.pid ]; then
  kill $(cat /tmp/celery_beat.pid) && rm /tmp/celery_beat.pid
fi

ps 
echo "All services stopped"