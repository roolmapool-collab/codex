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


def post_json(url, token, body):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    return request(req)


def get_json(url, token):
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="GET",
    )
    return request(req)


def request(req):
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return {"http_status": resp.status, "body": parse_json(body)}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"http_status": exc.code, "body": parse_json(body)}
    except Exception as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


def parse_json(text):
    try:
        return json.loads(text)
    except Exception:
        return text[:1000]


env = load_env()
token = env.get("MINIMAX_API_KEY") or os.environ.get("MINIMAX_API_KEY", "")
print(json.dumps({
    "token_present": bool(token),
    "token_prefix": token[:6] + "***" if token else "",
    "env_minimax_base_url": env.get("MINIMAX_BASE_URL", ""),
}, indent=2))

if token:
    print("TOKEN_PLAN_REMAINS")
    print(json.dumps(get_json("https://www.minimax.io/v1/token_plan/remains", token), indent=2, ensure_ascii=False))
    print("GET_VOICE")
    print(json.dumps(post_json("https://api.minimax.io/v1/get_voice", token, {"voice_type": "all"}), indent=2, ensure_ascii=False))
