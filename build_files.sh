#!/bin/bash
# CyberShield AI - Vercel Build Script

export PIP_BREAK_SYSTEM_PACKAGES=1

echo "--- Installing Python Dependencies ---"
python3 -m pip install -r requirements.txt --break-system-packages

echo "--- Collecting Static Files ---"
python3 manage.py collectstatic --noinput --clear || true

echo "--- Vercel Build Complete ---"
