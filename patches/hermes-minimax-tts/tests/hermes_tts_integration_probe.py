#!/usr/bin/env python3
import json
import os
from pathlib import Path

from tools.tts_tool import text_to_speech_tool

out = "/opt/data/audio_cache/minimax_hermes_test.mp3"
result = text_to_speech_tool("test", out)
print(result)
path = Path(out)
print(json.dumps({
    "exists": path.exists(),
    "size": path.stat().st_size if path.exists() else 0,
}, indent=2))
