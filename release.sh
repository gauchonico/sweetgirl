#!/bin/bash
set -e
npm install
npm run build
python manage.py migrate
python manage.py collectstatic --noinput
