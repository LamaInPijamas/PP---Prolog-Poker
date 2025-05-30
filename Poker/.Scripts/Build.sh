#!/bin/bash

function createVenv(){
  PATH_TO_LOGIC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../"
  PATH_TO_CURRENT_DIR="$(pwd)"
  cd "$PATH_TO_LOGIC_DIR" || exit 1
  python -m venv .venv
  "${PATH_TO_LOGIC_DIR}$1" install -r requirements.txt
  cd "$PATH_TO_CURRENT_DIR" || exit 1
}


# Main
case "$OSTYPE" in
  linux-gnu* ) createVenv ".venv/bin/pip" ;;
  darwin* ) createVenv ".venv/bin/pip" ;;
  msys* | cygwin* | win32* ) createVenv ".venv/Scripts/pip.exe" ;;
  * )
    echo "Unsupported OS: $OSTYPE"
    exit 1
    ;;
esac