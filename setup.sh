#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python -m venv $SCRIPT_DIR/.venv
$SCRIPT_DIR/.venv/bin/pip install -r $SCRIPT_DIR/requirements.txt
echo "init..."
echo -n "ACCOUNT:"
read ac
echo -n "PASSWORD:"
read -s ps
envfile=$SCRIPT_DIR/.env
echo "ac=$ac" >$envfile
echo "ps=$ps" >>$envfile
echo

if [[ ":$PATH:" != *":/usr/local/bin:"* ]]; then
  echo "export PATH=\$PATH:$SCRIPT_DIR" >>~/.bashrc
  source ~/.bashrc
fi
