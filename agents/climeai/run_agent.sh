#!/usr/bin/env bash
set -e

fatal () {
    echo "$1" >&2
    exit 1
}

PYTHON_SCRIPT="main.py"

# Determine script directory
SCRIPT_DIR=$(dirname "$(realpath "$0" 2>/dev/null || readlink -f "$0" 2>/dev/null || echo "$0")")

PROJECT_DIR="$SCRIPT_DIR"
echo "Agent directory: $PROJECT_DIR"

# Change to project directory
cd "$PROJECT_DIR" || fatal "Could not cd to '$PROJECT_DIR'"

# Install dependencies directly
echo "Installing dependencies directly..."
pip install fastapi langchain langchain-aimlapi langchain-community langchain-core \
    langchain-google-genai langchain-groq langchain-mistralai langgraph \
    langgraph-checkpoint-mongodb pyjwt sqlmodel uvicorn pymongo python-dotenv requests || fatal "Failed to install dependencies"

# Install uv
echo "Installing uv..."
pip install uv || fatal "Failed to install uv"

# Make sure the current directory is in PYTHONPATH
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

echo "Starting uvicorn server..."
uv run uvicorn main:app --reload --port 8000