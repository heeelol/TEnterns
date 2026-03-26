#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/4] Installing system packages (requires sudo)..."
sudo apt update
sudo apt install -y python3-pip python3-venv python3-opencv v4l-utils

echo "[2/4] Creating virtual environment at .venv (if missing)..."
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

echo "[3/4] Activating virtual environment and installing Python dependencies..."
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

echo "[4/4] Verifying key imports..."
python -c "import cv2, kitting_cv; print('Jetson venv setup OK')"

echo
echo "Setup complete."
echo "To use this environment in a new shell:"
echo "  cd $ROOT_DIR"
echo "  source .venv/bin/activate"
echo "  python scripts/run_local.py"
