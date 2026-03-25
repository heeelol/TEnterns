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

## Setup (Windows + Conda)

### 1) Open terminal in project root

```powershell
cd C:\Users\chenx\Documents\TEnterns\kitting-error-tracker
```

### 2) Create environment (first time only)

```powershell
conda env create -f environment.yml
```

### 3) Activate environment

```powershell
conda activate kitting-cv
```

### 4) Verify interpreter + packages

```powershell
python --version
python -c "import cv2, mediapipe; print('OpenCV + MediaPipe OK')"
```

## Run the Camera Pipeline

```powershell
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

## Daily Use

```powershell
cd C:\Users\chenx\Documents\TEnterns\kitting-error-tracker
conda activate kitting-cv
python scripts/run_local.py
```

## Next Implementation Steps

1. Replace `BinSegmenter.segment(...)` with your trained segmentation model inference.
2. Add stable bin ID mapping from contours.
3. Connect hand trajectory + grab state to kitting rule checks.
4. Log kitting errors (wrong bin / missed pick / extra pick).
