#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

# ------------------------------------------------------------------------------
# 0. Auto‑initialize a Poetry project if no pyproject.toml is found.
#
#    This runs:
#      poetry init --no-interaction --name "<current-directory-name>"
#
#    The --no-interaction flag tells Poetry not to prompt for input.
#    The --name flag sets the project name to the current directory’s basename.
# ------------------------------------------------------------------------------
if [ ! -f "pyproject.toml" ]; then
  echo "pyproject.toml not found. Initializing a new Poetry project..."
  PROJECT_NAME=$(basename "$PWD")
  poetry init --no-interaction --name "$PROJECT_NAME"
  echo "Created pyproject.toml with project name: $PROJECT_NAME"
fi

# ------------------------------------------------------------------------------
# 1. Configure Poetry to use an in-project virtual environment.
#
#    This creates the virtual environment in the project folder as .venv.
# ------------------------------------------------------------------------------
echo "Configuring Poetry to use an in-project virtual environment..."
poetry config virtualenvs.in-project true --local

# ------------------------------------------------------------------------------
# 2. Remove the existing virtual environment (if any).
# ------------------------------------------------------------------------------
if [ -d ".venv" ]; then
  echo "Removing existing virtual environment (.venv)..."
  rm -rf .venv
else
  echo "No existing virtual environment found."
fi

# ------------------------------------------------------------------------------
# 3. Create a new virtual environment and install dependencies.
#    This reads your pyproject.toml file and installs the listed packages.
# ------------------------------------------------------------------------------
echo "Creating a new virtual environment and installing dependencies with Poetry..."
poetry install --no-cache

# ------------------------------------------------------------------------------
# 4. Activate the new virtual environment.
# ------------------------------------------------------------------------------
echo "Activating the new virtual environment..."
# shellcheck disable=SC1091
source .venv/bin/activate

# ------------------------------------------------------------------------------
# 5. Optionally install additional packages from requirements.txt.
#    (If you have a requirements.txt in addition to pyproject.toml.)
# ------------------------------------------------------------------------------
if [ -f "requirements.txt" ]; then
  echo "Installing packages from requirements.txt..."
  pip install --upgrade pip
  pip install -r requirements.txt
fi

# ------------------------------------------------------------------------------
# 6. Update Windsurf to use the new virtual environment.
#
#    This example updates a configuration file (windsurf.conf) by replacing a line
#    that starts with PYTHON_ENV= to point to the new venv’s Python interpreter.
#    Adjust this section to match how Windsurf is configured in your environment.
# ------------------------------------------------------------------------------
WINDSURF_CONFIG_FILE="windsurf.conf"  # <-- Adjust if needed.
if [ -f "$WINDSURF_CONFIG_FILE" ]; then
  echo "Updating Windsurf configuration to use the new virtual environment..."
  sed -i.bak "s|^PYTHON_ENV=.*|PYTHON_ENV=$(pwd)/.venv/bin/python|" "$WINDSURF_CONFIG_FILE"
  echo "Windsurf configuration updated in $WINDSURF_CONFIG_FILE."
else
  echo "Windsurf configuration file ($WINDSURF_CONFIG_FILE) not found."
  echo "Please configure Windsurf manually to use: $(pwd)/.venv/bin/python"
fi

echo "Reset complete. The virtual environment is active."

# playwright install