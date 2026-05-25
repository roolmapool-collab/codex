#!/usr/bin/env python3
import json
import os
import urllib.error
import urllib.request


def load_env(path="/opt/data/.env"):
    values = {}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return values


def post_tts(token, voice_id):
    payload = {
        "model": "speech-2.8-hd",
        "text": "test",
        "stream": False,
        "language_boost": "French",
        "output_format": "url",
        "voice_setting": {
            "voice_id": voice_id,
            "speed": 1,
            "vol": 1,
            "pitch": 0,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
    }
    req = urllib.request.Request(
        "https://api.minimax.io/v1/t2a_v2",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8", errors="replace"))
            return summarize(resp.status, body)
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(text)
        except Exception:
            body = text[:1000]
        return summarize(exc.code, body)
    except Exception as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


def summarize(status, body):
    if isinstance(body, dict):
        body = dict(body)
        data = body.get("data")
        if isinstance(data, dict) and data.get("audio"):
            data["audio"] = "<present-redacted>"
        return {
            "http_status": status,
            "base_resp": body.get("base_resp"),
            "extra_info": body.get("extra_info"),
            "data": data,
            "trace_id": body.get("trace_id"),
        }
    return {"http_status": status, "body": body}


env = load_env()
token = env.get("MINIMAX_API_KEY") or os.environ.get("MINIMAX_API_KEY", "")
voices = [
    "French_MaleNarrator",
    "moss_audio_c23f7c1c-53ab-11f1-83ef-8afcbb8b5b5c",
]
for voice in voices:
    print(f"TTS_TEST {voice}")
    print(json.dumps(post_tts(token, voice), indent=2, ensure_ascii=False))
