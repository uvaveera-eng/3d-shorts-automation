# 3D Animated Shorts Automation 🎬

An automated, serverless cloud pipeline that creates and publishes viral, high-retention 3D explainer shorts (*Zack D. Films* style) to **YouTube Shorts**, **Instagram Reels**, and **Facebook Page Reels** with **$0 API costs**.

---

## ⚡ Architecture & Pipeline

| Stage | Technology | Function |
| :--- | :--- | :--- |
| **Cloud Execution** | GitHub Actions (Ubuntu) | Runs headlessly on cloud runners for $0. |
| **Story & Script** | Google Gemini 2.5 Flash / Curated Pool | Writes hook-driven, deduplicated "What happens if...?" explainer scripts. |
| **Voiceover (TTS)** | Kokoro-82M (`kokoro-onnx`) | Offline neural TTS with human-like breathing and natural pauses. |
| **Word Alignment** | Faster-Whisper (`small.en`) | Generates millisecond-accurate word timestamps for karaoke subtitles. |
| **3D & Visuals** | Three.js + WebGL + Canvas | Programmatically animates 3D models, organs, blood vessels, and camera movements. |
| **Frame Capture** | Headless Chrome (Node.js 22+) | Captures 1080×1920 frames at 30 fps. |
| **Sound Design** | Procedural Audio (`mix.py`) | Mathematically generates and syncs impact thuds, risers, and sound cues. |
| **Encoding** | FFmpeg (libx264, aac) | Compiles frames and audio mix into vertical Full HD MP4. |
| **Publishing** | YouTube Data API & Meta Graph API | Publishes directly to YouTube, Instagram Reels, and Facebook Page. |

---

## 🔑 GitHub Secrets Configuration

Add the following secrets to your GitHub repository under **Settings > Secrets and variables > Actions**:

* `GEMINI_API_KEY`: *(Optional)* Your Google Gemini API key for dynamic AI script generation.
* `FB_PAGE_ID`: Your Facebook Page ID.
* `FB_PAGE_TOKEN`: Your Facebook Page Access Token.
* `IG_USER_ID`: Your Instagram Professional User ID.
* `IG_ACCESS_TOKEN`: Your Instagram Graph API Access Token.
* `YOUTUBE_CLIENT_ID`: Google Cloud OAuth2 Client ID.
* `YOUTUBE_CLIENT_SECRET`: Google Cloud OAuth2 Client Secret.
* `YOUTUBE_REFRESH_TOKEN`: YouTube Data API v3 Refresh Token.

---

## ⏰ Automated Scheduling with cronjob.org

Trigger the workflow at your exact chosen hours (e.g. 9:00 AM, 2:00 PM, 9:00 PM):

* **Endpoint**: `https://api.github.com/repos/uvaveera-eng/3d-shorts-automation/actions/workflows/3d_shorts_pipeline.yml/dispatches`
* **Method**: `POST`
* **Headers**:
  * `Accept: application/vnd.github.v3+json`
  * `Authorization: Bearer <GITHUB_PERSONAL_ACCESS_TOKEN>`
  * `User-Agent: cronjob-dispatcher`
  * `Content-Type: application/json`
* **Body**:
  ```json
  {
    "ref": "main"
  }
  ```
