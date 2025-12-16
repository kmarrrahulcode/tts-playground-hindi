#!/bin/bash

echo "Checking specific virtual environments for TTS Playground..."

# Function to check and create venv
ensure_venv() {
    local venv_path=$1
    local req_file=$2

    if [ -d "$venv_path" ]; then
        echo "  [SKIP] '$venv_path' already exists."
    else
        echo "  [CREATE] Creating '$venv_path'..."
        python3 -m venv "$venv_path"
        
        # Check for pip in bin (Unix/Linux/MacOS naming convention)
        if [ -f "$venv_path/bin/pip" ]; then
             echo "  [INSTALL] Installing dependencies from '$req_file'..."
             "$venv_path/bin/pip" install -r "$req_file"
             echo "  [DONE] Setup complete for '$venv_path'."
        # Check for pip in Scripts (Windows Git Bash sometimes uses this layout depending on python install)
        elif [ -f "$venv_path/Scripts/pip" ]; then
             echo "  [INSTALL] Installing dependencies from '$req_file'..."
             "$venv_path/Scripts/pip" install -r "$req_file"
             echo "  [DONE] Setup complete for '$venv_path'."
        else
             echo "  [ERROR] Failed to find pip at '$venv_path/bin/pip' or '$venv_path/Scripts/pip'. Virtual environment creation might have failed."
        fi
    fi
}

# 1. Standard venv
echo -e "\n1. Standard Environment (venv)"
ensure_venv "venv" "requirements.txt"

# 2. Indri venv
echo -e "\n2. Indri Environment (venv-indri)"
ensure_venv "venv-indri" "requirements-indri.txt"

echo -e "\nAll checks complete. Environments are ready if no errors occurred."
