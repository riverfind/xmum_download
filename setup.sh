#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python -m venv .venv
.venv/bin/pip install -r requirements.txt
echo "init..."
echo -n "ACCOUNT:"
read ac
echo -n "PASSWORD:"
read ps
echo "ac=$ac" >./.env
echo "ps=$ps" >>./.env
