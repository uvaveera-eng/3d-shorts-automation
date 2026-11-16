import os
import sys
import json
import shutil
import subprocess
import argparse
from pathlib import Path

# Fix Windows console UTF-8 output encoding
try:
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# Add project root to sys.path so we can import existing uploaders
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from pipeline_3d.generator import generate_3d_script

try:
    from uploader import post_to_facebook_reels, post_to_instagram_reels
    from youtube_uploader import upload_youtube_short
except ImportError:
    post_to_facebook_reels = None
    post_to_instagram_reels = None
    upload_youtube_short = None


def load_3d_state(state_file: str) -> dict:
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data.setdefault("past_topics", [])
                    return data
        except Exception as e:
            print(f"[WARN] Error loading {state_file}: {e}")
    return {"past_topics": []}


def save_3d_state(state_file: str, state: dict):
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def render_phase(base_dir: str):
    print("=" * 65)
    print("🎬 PHASE 1: GENERATING & RENDERING 3D SHORT (KOKORO + CHROME + FFMPEG)")
    print("=" * 65)

    pipeline_dir = Path(base_dir) / "pipeline_3d"
    engine_dir = pipeline_dir / "engine"
    scripts_dir = pipeline_dir / "scripts"
    state_file = str(pipeline_dir / "state_3d.json")
    meta_file = str(Path(base_dir) / "metadata.json")
    final_output_mp4 = str(Path(base_dir) / "final_reel.mp4")

    gemini_key = (os.environ.get("GEMINI_API_KEY") or "").strip()
    fps = os.environ.get("FPS", "30")

    # 1. Load state and generate script
    state = load_3d_state(state_file)
    print("\n[STEP 1] Generating Script with Topic Deduplication...")
    script_data = generate_3d_script(gemini_key, state.get("past_topics", []))
    topic = script_data.get("title", "What Happens If...?")

    # Write script.json to engine
    script_path = engine_dir / "script.json"
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2)
    print(f"  -> Saved script to {script_path}")

    # 2. Synthesize Voiceover via Kokoro TTS
    print("\n[STEP 2] Synthesizing Studio Voiceover (Kokoro-82M TTS)...")
    voice_py = str(scripts_dir / "voice.py")
    subprocess.run([sys.executable, voice_py, str(engine_dir)], check=True)

    # 3. Whisper Word Alignment
    print("\n[STEP 3] Pinning Millisecond Subtitle Alignment (Whisper AI)...")
    words_py = str(scripts_dir / "words.py")
    subprocess.run([sys.executable, words_py, str(engine_dir)], check=True)

    # 4. Sound Design & Cue Mix
    print("\n[STEP 4] Synthesizing Procedural Audio Cues & Sound Bed...")
    capture_mjs = str(engine_dir / "tools" / "capture.mjs")
    mix_py = str(engine_dir / "tools" / "mix.py")
    subprocess.run(["node", capture_mjs, "cues"], cwd=str(engine_dir), check=True)
    subprocess.run([sys.executable, mix_py, str(engine_dir)], cwd=str(engine_dir), check=True)
    print("  -> Mixed data/mix.wav with procedural audio cues")

    # 5. Headless Chrome 3D Canvas Capture + FFmpeg Video Encoding
    print(f"\n[STEP 5] Headless 3D Render at 1080x1920 @ {fps}fps...")
    renders_dir = engine_dir / "renders"
    renders_dir.mkdir(exist_ok=True)
    render_target = str(renders_dir / "output.mp4")

    env = os.environ.copy()
    env["FPS"] = str(fps)
    subprocess.run(["node", capture_mjs, "video", render_target], cwd=str(engine_dir), env=env, check=True)

    # Copy output to root final_reel.mp4
    shutil.copy2(render_target, final_output_mp4)
    print(f"\n[SUCCESS] Rendered final 3D short to: {final_output_mp4}")

    # Prepare metadata for publishing
    meta_info = script_data.get("metadata", {})
    metadata = {
        "title": meta_info.get("title", f"{topic} #shorts"),
        "description": meta_info.get("description", f"{topic}\n\n#shorts #science #facts"),
        "topic": topic,
        "part": 1,
        "badge": "WHAT IF",
        "tags": meta_info.get("tags", ["shorts", "science", "facts", "animation"])
    }
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # Update state history
    state["past_topics"].append(topic)
    save_3d_state(state_file, state)
    print(f"  -> Updated {state_file} with topic '{topic}'")


def publish_phase(base_dir: str, video_url: str):
    print("=" * 65)
    print("🚀 PHASE 2: MULTI-PLATFORM PUBLISHING (YOUTUBE, INSTA, FB)")
    print("=" * 65)

    meta_file = Path(base_dir) / "metadata.json"
    local_video = str(Path(base_dir) / "final_reel.mp4")

    if not meta_file.exists():
        raise FileNotFoundError(f"Missing {meta_file}")

    with open(meta_file, "r", encoding="utf-8") as f:
        meta = json.load(f)

    title = meta["title"]
    description = meta["description"]
    topic = meta["topic"]

    fb_page_id = os.environ.get("FB_PAGE_ID")
    fb_token = os.environ.get("FB_PAGE_TOKEN")
    ig_user_id = os.environ.get("IG_USER_ID")
    ig_token = os.environ.get("IG_ACCESS_TOKEN")

    # 1. Facebook Page Reels Upload
    if fb_page_id and fb_token and os.path.exists(local_video) and post_to_facebook_reels:
        try:
            print("\n[1] Uploading to Facebook Page Reels...")
            fb_res = post_to_facebook_reels(fb_page_id, fb_token, local_video, title, description)
            print("  Facebook Result:", fb_res)
        except Exception as e:
            print(f"  Facebook Upload Error: {e}")

    # 2. Instagram Reels Upload
    if video_url and ig_user_id and ig_token and post_to_instagram_reels:
        try:
            print("\n[2] Uploading to Instagram Reels...")
            ig_res = post_to_instagram_reels(ig_user_id, ig_token, video_url, f"{title}\n\n{description}")
            print("  Instagram Result:", ig_res)
        except Exception as e:
            print(f"  Instagram Upload Error: {e}")

    # 3. YouTube Shorts Upload
    yt_client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    yt_client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    yt_refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if yt_client_id and yt_client_secret and yt_refresh_token and os.path.exists(local_video) and upload_youtube_short:
        try:
            print("\n[3] Uploading to YouTube Shorts...")
            yt_res = upload_youtube_short(
                local_video,
                title=title,
                description=description,
                client_id=yt_client_id,
                client_secret=yt_client_secret,
                refresh_token=yt_refresh_token
            )
            print("  YouTube Shorts Result:", yt_res)
        except Exception as e:
            print(f"  YouTube Upload Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="3D Shorts Automated Pipeline")
    parser.add_argument("--render-only", action="store_true", help="Generate and render video only")
    parser.add_argument("--publish-only", type=str, help="Publish with provided video URL")
    args = parser.parse_args()

    base_dir = str(ROOT_DIR)

    if args.publish_only:
        publish_phase(base_dir, args.publish_only)
    elif args.render_only:
        render_phase(base_dir)
    else:
        render_phase(base_dir)
        video_url = os.environ.get("PUBLIC_VIDEO_URL", "")
        publish_phase(base_dir, video_url)


if __name__ == "__main__":
    main()
