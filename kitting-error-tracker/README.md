# Kitting Error Tracker (Starter)

Computer-vision starter pipeline for kitting-error detection using:
- MediaPipe hand tracking (no training required)
- Bin segmentation placeholder (to be replaced by your model)

This project uses a **Conda-first workflow**.

## Current Features

- Tracks up to **2 hands** in real time.
- Displays all **21 landmarks** per hand.
- Shows per-hand **grab status** (`GRAB`/`OPEN`) and a `grab_score`.
- Shows `Hands detected: N` on the live frame.
- Displays a `bin-mask` window from the placeholder segmenter.

## Project Structure

```text
kitting-error-tracker/
├─ configs/
│  └─ pipeline.yaml
├─ data/
│  ├─ raw/
│  └─ processed/
├─ models/
├─ environment.yml
├─ scripts/
│  └─ run_local.py
│  └─ setup_jetson_venv.sh
├─ src/
│  └─ kitting_cv/
│     ├─ tracking/
│     │  └─ mediapipe_tracker.py
│     ├─ segmentation/
│     │  └─ bin_segmenter.py
│     └─ pipeline/
│        └─ run_pipeline.py
├─ requirements.txt
└─ pyproject.toml
```

## First-Time Setup (Windows + Conda)

Run these once:

### 1) Open terminal in project root

```powershell
cd C:\Users\chenx\Documents\TEnterns\kitting-error-tracker
```

### 2) Create Conda environment

```powershell
conda env create -f environment.yml
```

### 3) Activate Conda environment

```powershell
conda activate kitting-cv
```

### 4) Install this project package (required)

```powershell
python -m pip install -e .
```

### 5) Verify interpreter + packages

```powershell
python -c "import sys; print(sys.executable)"
python -c "import cv2, mediapipe, kitting_cv; print('Environment OK')"
```

If you see `(.venv)` in your prompt, run `deactivate` so only `(kitting-cv)` is active.

## Run After Setup (Daily Use)

Each time you start working:

```powershell
cd C:\Users\chenx\Documents\TEnterns\kitting-error-tracker
conda activate kitting-cv
python scripts/run_local.py
```

Press `q` to close the windows.

## Expected Output On Screen

- `kitting-camera` window:
	- Hand count (`Hands detected: 0/1/2`)
	- Two-hand landmark overlays (index labels for all 21 points)
	- `Hand 1 ... GRAB/OPEN score=...`
	- `Hand 2 ... GRAB/OPEN score=...`
- `bin-mask` window:
	- Placeholder segmentation mask output

## Troubleshooting

### Conda not recognized

Run in Anaconda Prompt:

```powershell
conda init powershell
```

Then close/reopen VS Code.

### Wrong environment is active

Check executable path:

```powershell
python -c "import sys; print(sys.executable)"
```

It should point to `...\.conda\envs\kitting-cv\python.exe`.

### MediaPipe import/API mismatch

This project pins MediaPipe in `requirements.txt` for compatibility.
If needed, reinstall inside `kitting-cv`:

```powershell
pip install --upgrade --force-reinstall mediapipe==0.10.14
```

### Camera cannot open

Try a different camera index:

```powershell
python -c "from kitting_cv.pipeline import run_camera_pipeline; run_camera_pipeline(camera_index=1)"
```

Close other apps that may lock the camera (Teams/Zoom/browser).

## Jetson (ICAM-520 / NVIDIA Jetson) Quick Setup

You do **not** need Conda on Jetson. Use a local `venv` unless you specifically want Conda.

### One-command setup (recommended)

```bash
cd ~/kitting-error-tracker
bash scripts/setup_jetson_venv.sh
```

Then run:

```bash
source .venv/bin/activate
python scripts/run_local.py
```

### Manual setup (same steps as script)

#### 1) Install system packages

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv python3-opencv v4l-utils
```

#### 2) Create and activate a virtual environment

```bash
cd ~/kitting-error-tracker
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

#### 3) Install project dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

#### 4) Verify imports and camera

```bash
python -c "import cv2; print(cv2.__version__)"
python -c "import mediapipe, kitting_cv; print('Jetson environment OK')"
v4l2-ctl --list-devices
```

#### 5) Run

```bash
python scripts/run_local.py
```

If `mediapipe` is not available on your JetPack/Python combination, keep the same project structure and replace the hand-tracking backend with a Jetson-friendly option.

## Next Implementation Steps

1. Replace `BinSegmenter.segment(...)` with your trained segmentation model inference.
2. Add stable bin ID mapping from contours.
3. Connect hand trajectory + grab state to kitting rule checks.
4. Log kitting errors (wrong bin / missed pick / extra pick).
