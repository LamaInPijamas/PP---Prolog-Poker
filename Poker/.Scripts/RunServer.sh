#!/bin/bash

# Execute 
function executeController(){
  PATH_TO_LOGIC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../"
  PATH_TO_CURRENT_DIR="$(pwd)"
  cd "$PATH_TO_LOGIC_DIR/Core/" || exit 1
  "${PATH_TO_LOGIC_DIR}$1" ../Server.py
  cd "$PATH_TO_CURRENT_DIR" || exit 1
}


# Main
case "$OSTYPE" in
  linux-gnu* ) executeController ".venv/bin/python" ;;
  darwin* ) executeController ".venv/bin/python" ;;
  msys* | cygwin* | win32* ) executeController ".venv/Scripts/python.exe" ;;
  * )
    echo "Unsupported OS: $OSTYPE"
    exit 1
    ;;
esac