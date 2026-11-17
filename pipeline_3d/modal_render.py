import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
import modal

app = modal.App("3d-shorts-renderer")

# Build lightweight Debian image with Chrome, Node 22, FFmpeg, and Python AI libs
image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install(
        "curl",
        "wget",
        "gnupg",
        "ffmpeg",
        "fonts-dejavu-core",
        "xvfb",
        "ca-certificates",
    )
    .run_commands(
        "curl -fsSL https://deb.nodesource.com/setup_22.x | bash -",
        "apt-get install -y nodejs",
        "wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg",
        'echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list',
        "apt-get update -qq",
        "apt-get install -y google-chrome-stable",
        "mkdir -p /root/.faceless-shorts/kokoro",
        "curl -L https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx -o /root/.faceless-shorts/kokoro/kokoro-v1.0.onnx",
        "curl -L https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin -o /root/.faceless-shorts/kokoro/voices-v1.0.bin"
    )
    .pip_install("numpy", "scipy", "kokoro-onnx", "faster-whisper", "requests")
    .add_local_dir(Path(__file__).parent, remote_path="/root/pipeline_3d")
)


@app.function(
    image=image,
    gpu="T4",
    timeout=600,
)
def render_video_gpu(script_data: dict, shots_code: str = None, fps: int = 30) -> dict:
    """Renders the 3D video using an Nvidia T4 GPU on Modal."""
    base_dir = "/root/pipeline_3d"
    engine_dir = os.path.join(base_dir, "engine")
    scripts_dir = os.path.join(base_dir, "scripts")

    # 1. Write script.json and custom shots.js
    script_path = os.path.join(engine_dir, "script.json")
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2)

    if shots_code:
        shots_path = os.path.join(engine_dir, "src", "shots.js")
        with open(shots_path, "w", encoding="utf-8") as f:
            f.write(shots_code)

    # 2. Voiceover (Kokoro)
    voice_py = os.path.join(scripts_dir, "voice.py")
    subprocess.run(["python3", voice_py, engine_dir], check=True)

    # 3. Whisper Subtitles
    words_py = os.path.join(scripts_dir, "words.py")
    subprocess.run(["python3", words_py, engine_dir], check=True)

    # 4. Sound cues & mix
    capture_mjs = os.path.join(engine_dir, "tools", "capture.mjs")
    mix_py = os.path.join(engine_dir, "tools", "mix.py")
    subprocess.run(["xvfb-run", "-a", "node", capture_mjs, "cues"], cwd=engine_dir, check=True)
    subprocess.run(["python3", mix_py, engine_dir], cwd=engine_dir, check=True)

    # 5. Headless Chrome GPU Render
    output_mp4 = os.path.join(engine_dir, "renders", "output.mp4")
    os.makedirs(os.path.dirname(output_mp4), exist_ok=True)
    env = os.environ.copy()
    env["FPS"] = str(fps)
    env["USE_GPU"] = "1"

    subprocess.run(
        ["xvfb-run", "-a", "node", capture_mjs, "video", output_mp4],
        cwd=engine_dir,
        env=env,
        check=True
    )

    with open(output_mp4, "rb") as f:
        video_bytes = f.read()

    return {"video_bytes": video_bytes, "size": len(video_bytes)}
