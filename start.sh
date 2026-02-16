#!/bin/bash
export FLASK_APP=app.py
exec gunicorn app:app
