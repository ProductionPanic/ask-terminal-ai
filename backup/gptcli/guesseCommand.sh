#!/bin/bash
THIS_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$THIS_SCRIPT_DIR"
ACTIVATED_FILE="$THIS_SCRIPT_DIR/activated"
if [ ! -f "$ACTIVATED_FILE" ]; then
  echo "Installing dependencies..."
  bash "$THIS_SCRIPT_DIR/install.sh" > /dev/null
  echo "Done."
fi

python cli.py $@

