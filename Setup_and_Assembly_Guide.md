# Setup & Assembly Guide (Manim CE, Voice-Over, Music & FFmpeg)

This guide walks you through installing all required tools, generating or recording the voice-over, merging audio with the rendered 1080p video, and mixing low-volume background music cleanly.

---

## 1. Prerequisites & Installation

### macOS (Apple Silicon / Intel via Homebrew)
```bash
# 1. Install system dependencies (Cairo, Pango, pkg-config, FFmpeg)
brew install cairo pango pkg-config ffmpeg

# 2. Install LaTeX (required by Manim for MathTex and Matrix)
# Option A (Lightweight, ~150 MB, no sudo required if unpacked to ~/Library/TinyTeX):
curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" | sh
# Ensure dvisvgm and required math packages are installed:
tlmgr install dvisvgm standalone preview amsmath amsfonts xcolor ec lm cm-super babel-english

# Option B (Full MacTeX via Homebrew Cask, ~4 GB):
# brew install --cask mactex-no-gui

# 3. Create Python virtual environment and install Manim Community Edition (v0.18+)
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install manim
```

### Linux (Ubuntu / Debian)
```bash
sudo apt update
sudo apt install -y build-essential python3-dev libcairo2-dev libpango1.0-dev ffmpeg \
  texlive-latex-base texlive-fonts-recommended texlive-latex-extra dvisvgm
python3 -m venv .venv
source .venv/bin/activate
pip install manim
```

### Windows
1. Install **Python 3.11+**, **FFmpeg** (`winget install Gyan.FFmpeg`), and **MiKTeX** (`winget install MiKTeX.MiKTeX`, enable auto-install packages on the fly).
2. In PowerShell:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install manim
   ```

---

## 2. Rendering the Video (1080p, 16:9, MP4)

Render individual scenes quickly at low quality while editing:
```bash
manim -pql Code/main.py Scene1_Hook
manim -pql Code/main.py Scene4_WorkedExample
```

Render the full 5:10 video at **1920×1080 (60 fps)**:
```bash
manim -qh --resolution 1920,1080 Code/main.py FullVideo
```

Manim outputs the silent rendered video to:
`media/videos/main/1080p60/FullVideo.mp4`

Copy it to your submission filename:
```bash
cp media/videos/main/1080p60/FullVideo.mp4 Shlok_Sharma_Video.mp4
```

*(Note: `Shlok Sharma` and `E25B070773` are already set in `Code/main.py`.)*

---

## 3. Recording or Generating the Voice-Over

### Option A: Your Own Voice Recording (Recommended for Viva Readiness)
1. Open **Audacity** (free) or **QuickTime / Voice Memos** in a quiet room.
2. Play `FullVideo.mp4` muted on screen and read `Narration_Script.md` along with the `[timestamp]` cues.
3. Export as WAV or high-bitrate MP3 (`voiceover.wav` or `voiceover.mp3`).
4. Optional cleanup in Audacity: **Effect → Noise Reduction** and **Effect → Loudness Normalization (-16 LUFS)**.

### Option B: Text-to-Speech (Optional)
- **macOS built-in `say`** or **Edge TTS (`pip install edge-tts`)**:
  ```bash
  # Example using edge-tts with a clear engineering-friendly voice
  edge-tts --voice en-US-AndrewNeural --file narration_plain.txt --write-media voiceover.mp3
  ```
- Or record scene-by-scene clips (`s1.wav` ... `s6.wav`) and align them cleanly in Audacity or DaVinci Resolve / CapCut / iMovie against the scene timestamps (`0:00`, `0:30`, `1:15`, `2:30`, `4:00`, `4:45`).

---

## 4. Merging Voice-Over & Video with FFmpeg

If your voice-over track (`voiceover.mp3`) matches the full ~5:10 timeline:

```bash
ffmpeg -i media/videos/main/1080p60/FullVideo.mp4 -i voiceover.mp3 \
  -c:v copy -c:a aac -b:a 192k -map 0:v:0 -map 1:a:0 -shortest \
  Shlok_Sharma_Video.mp4
```

---

## 5. Adding Low-Volume Background Music (10–15% Volume)

Pick a **Creative Commons (CC BY)** or **royalty-free** instrumental track (e.g., from Free Music Archive, Pixabay Music, or YouTube Audio Library — avoid tracks with lyrics).

Mix the voice-over at `100%` volume and background music at `12%` volume (`volume=0.12`), with a smooth 2-second fade-out at the end:

```bash
ffmpeg -i media/videos/main/1080p60/FullVideo.mp4 \
       -i voiceover.mp3 \
       -stream_loop -1 -i bg_music.mp3 \
  -filter_complex "\
    [1:a]aresample=44100,volume=1.0[vo]; \
    [2:a]aresample=44100,volume=0.12,afade=t=out:st=307:d=3[bgm]; \
    [vo][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]" \
  -map 0:v:0 -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest \
  Shlok_Sharma_Video.mp4
```
