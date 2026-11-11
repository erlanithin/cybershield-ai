#!/bin/bash
# CyberShield AI - Vercel Build Script

echo "--- Installing Python Dependencies ---"
python3 -m pip install -r requirements.txt

echo "--- Collecting Static Files ---"
python3 manage.py collectstatic --noinput --clear

echo "--- Running Database Migrations ---"
python3 manage.py migrate --noinput

echo "--- Vercel Build Complete ---"
