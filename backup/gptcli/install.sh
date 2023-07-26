#!/bin/bash
THIS_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$THIS_SCRIPT_DIR"
python3 -m venv venv
source venv/bin/activate
touch activated
python3 -m pip install -r ./requirements.txt
