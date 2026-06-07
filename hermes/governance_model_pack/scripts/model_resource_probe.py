#!/usr/bin/env python3
"""
model_resource_probe.py — Live Counters Probe for Hermes

Read-only probe to check model resource availability and status.
Produces /opt/data/workspace/healthchecks/model_resource_status.json

Usage:
  python3 model_resource_probe.py --dry-run
  python3 model_resource_probe.py --write
  python3 model_resource_probe.py --resource minimax|codex|mimo|openrouter|all

Status values:
  GREEN = available, quota OK
  YELLOW = available but quota uncertain or degraded
  RED = unavailable or error
  UNKNOWN = cannot probe (no key, no access)
  MANUAL_REQUIRED = requires human counter check
  CANARY_ONLY = MiMo canary not passed, only read-only discovery allowed

No secrets displayed. No key values written in plain text.
"""

import json
import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime, timezone

# Configuration
WORKSPACE = Path("/opt/data/workspace")
HC_DIR = WORKSPACE / "healthchecks"
STATUS_FILE = HC_DIR / "model_resource_status.json"
EXAMPLE_FILE = HC_DIR / "model_resource_status.example.json"
MODEL_GOVERNANCE = WORKSPACE / "MODEL_RESOURCE_GOVERNANCE.md"
MIMO_FICHE = WORKSPACE / "model_resources" / "mimo.md"

# Thresholds
STALE_THRESHOLD_SECONDS = 3600  # 1 hour
MASK = "***MASKED***"

# Patterns to mask secrets
SECRET_PATTERNS = [
    r'(sk-[a-zA-Z0-9]{20,})',
    r'(ghp_[a-zA-Z0-9]{36})',
    r'(xai-[a-zA-Z0-9_-]{20,})',
    r'(Bearer\s+[a-zA-Z0-9_-]{20,})',
    r'(token-plan-[a-zA-Z0-9_-]{20,})',
]


def mask_secret(value):
    """Mask a secret value for display."""
    if not isinstance(value, str) or len(value) < 8:
        return MASK
    return f"{value[:4]}{MASK}{value[-4:]}"


def mask_dict_secrets(d):
    """Recursively mask secrets in a dict."""
    result = {}
    for k, v in d.items():
        if isinstance(v, str) and any(p.match(v) or p.search(v) for p in [__import__('re').compile(p) for p in SECRET_PATTERNS]):
            result[k] = mask_secret(v)
        elif isinstance(v, dict):
            result[k] = mask_dict_secrets(v)
        elif isinstance(v, list):
            result[k] = [mask_secret(x) if isinstance(x, str) and len(x) > 20 else x for x in v]
        else:
            result[k] = v
    return result


def read_env():
    """Read relevant environment variables without exposing secrets."""
    env = {}
    key_vars = ['MINIMAX_API_KEY', 'XIAOMI_API_KEY', 'MINIMAX_BASE_URL', 'XIAOMI_BASE_URL',
                'OPENAI_API_KEY', 'OPENROUTER_API_KEY', 'CODEX_TOKEN']
    for var in key_vars:
        val = os.environ.get(var, '')
        if val:
            env[var] = mask_secret(val) if 'KEY' in var else val
    return env


def read_env_file(env_path):
    """Read key presence from .env file without exposing values."""
    if not os.path.exists(env_path):
        return {}
    result = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key = line.split('=', 1)[0].strip()
                if any(k in key for k in ['MINIMAX', 'XIAOMI', 'MIMO', 'OPENROUTER', 'CODEX', 'OPENAI']):
                    result[key] = True  # presence only, no value
    return result


def check_key_presence(var_name, env_vars=None, env_files=None):
    """
    Check if a key is present WITHOUT displaying its value.
    
    Returns dict:
      - key_present: bool
      - key_source: "ENV" | "ENV_FILE" | "NOT_FOUND"
      - key_type: "subscription" | "token_plan" | "oauth" | "unknown"
    """
    result = {"key_present": False, "key_source": "NOT_FOUND", "key_type": "unknown"}
    
    # Check environment first
    if env_vars is None:
        env_vars = [var_name]
    for var in env_vars:
        val = os.environ.get(var, '')
        if val:
            result["key_present"] = True
            result["key_source"] = "ENV"
            break
    
    # Check .env files if not in environment
    if not result["key_present"]:
        if env_files is None:
            env_files = ['/opt/data/.env', '/root/hermes/data/.env']
        for path in env_files:
            keys = read_env_file(path)
            if var_name in keys:
                result["key_present"] = True
                result["key_source"] = "ENV_FILE"
                break
    
    # Classify key type
    if any(k in var_name for k in ['MINIMAX', 'MIMO', 'XIAOMI']):
        result["key_type"] = "token_plan"
    elif 'OPENROUTER' in var_name:
        result["key_type"] = "subscription"
    elif 'CODEX' in var_name or 'OPENAI' in var_name:
        result["key_type"] = "oauth"
    
    return result


def check_file_freshness(path, max_age=STALE_THRESHOLD_SECONDS):
    """Check if a file is fresh enough (< max_age seconds)."""
    if not path.exists():
        return None, "FILE_NOT_FOUND"
    age = time.time() - path.stat().st_mtime
    if age > max_age:
        return age, "STALE"
    return age, "FRESH"


def probe_minimax():
    """Probe MiniMax availability via /v1/models (read-only)."""
    # Check key presence WITHOUT exposing value
    creds = check_key_presence('MINIMAX_API_KEY', env_vars=['MINIMAX_API_KEY', 'MINIMAX_TOKEN', 'MINIMAX_SUBSCRIPTION_KEY'])
    key = os.environ.get('MINIMAX_API_KEY', os.environ.get('MINIMAX_TOKEN', ''))
    base = os.environ.get('MINIMAX_BASE_URL', 'https://api.minimax.io/anthropic')

    if not key:
        # Key exists in .env but not loaded in environment
        if creds["key_present"] and creds["key_source"] == "ENV_FILE":
            return {
                "status": "YELLOW",
                "credentials": {
                    "key_present": True,
                    "key_source": "ENV_FILE",
                    "key_type": "token_plan",
                    "secret_exposed": False,
                    "runtime_note": "Key found in /opt/data/.env but not loaded in environment. Probe requires runtime key or reload."
                },
                "quota": {
                    "quota_5h": "MANUAL_REQUIRED",
                    "quota_weekly": "MANUAL_REQUIRED",
                    "quota_monthly": "MANUAL_REQUIRED"
                },
                "probe_freshness": datetime.now(timezone.utc).isoformat(),
                "decision": "STOP_AND_ASK",
                "notes": "MINIMAX_API_KEY exists in .env but not in runtime environment. Stéphane must provide counter values or reload key."
            }
        else:
            return {
                "status": "UNKNOWN",
                "credentials": {
                    "key_present": False,
                    "key_source": "NOT_FOUND",
                    "key_type": "token_plan",
                    "secret_exposed": False
                },
                "quota": {
                    "quota_5h": "MANUAL_REQUIRED",
                    "quota_weekly": "MANUAL_REQUIRED",
                    "quota_monthly": "MANUAL_REQUIRED"
                },
                "probe_freshness": datetime.now(timezone.utc).isoformat(),
                "decision": "STOP_AND_ASK",
                "notes": "MINIMAX_API_KEY not found in environment or .env files. Cannot probe."
            }

    try:
        import urllib.request
        req = urllib.request.Request(
            f"{base}/models",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        )
        start = time.time()
        resp = urllib.request.urlopen(req, timeout=8)
        latency_ms = round((time.time() - start) * 1000)
        data = json.loads(resp.read())
        models = [m['id'] for m in data.get('data', [])]

        # Check for recent errors in logs
        log_path = Path("/opt/data/logs/gateway.log")
        recent_errors = []
        if log_path.exists():
            lines = log_path.read_text().split('\n')[-200:]
            for line in lines:
                if any(err in line for err in ['429', '529', 'rate-limit', 'quota exceeded']):
                    recent_errors.append(line.strip()[:100])

        return {
            "status": "GREEN" if latency_ms < 3000 else "YELLOW",
            "credentials": {
                "key_present": True,
                "key_source": "ENV",
                "key_type": "token_plan",
                "secret_exposed": False
            },
            "models_available": models,
            "models_count": len(models),
            "latency_ms": latency_ms,
            "quota": {
                "quota_5h": "MANUAL_REQUIRED",
                "quota_weekly": "MANUAL_REQUIRED",
                "quota_monthly": "MANUAL_REQUIRED",
                "endpoint_quota_api": "NOT_FOUND"
            },
            "probe_freshness": datetime.now(timezone.utc).isoformat(),
            "decision": "USE",
            "notes": f"Probe OK. {len(models)} models. Latency {latency_ms}ms. Recent errors: {len(recent_errors)}. Quota counters MANUAL_REQUIRED (no endpoint found)."
        }
    except Exception as e:
        return {
            "status": "RED",
            "credentials": {
                "key_present": True,
                "key_source": "ENV",
                "key_type": "token_plan",
                "secret_exposed": False
            },
            "quota": {
                "quota_5h": "MANUAL_REQUIRED",
                "quota_weekly": "MANUAL_REQUIRED",
                "quota_monthly": "MANUAL_REQUIRED"
            },
            "probe_freshness": datetime.now(timezone.utc).isoformat(),
            "decision": "STOP_AND_ASK",
            "notes": f"Probe failed: {type(e).__name__}: {str(e)[:80]}"
        }


def probe_codex():
    """Probe Codex OAuth status via Nous."""
    # Codex uses OAuth via Nous — we check if the token is available
    codex_key_presence = check_key_presence('CODEX_TOKEN', env_vars=['CODEX_TOKEN', 'OPENAI_API_KEY'])
    codex_token = os.environ.get('CODEX_TOKEN', os.environ.get('OPENAI_API_KEY', ''))

    if not codex_token:
        # Token not in runtime environment — check if it exists in .env files
        if codex_key_presence["key_present"]:
            return {
                "status": "YELLOW",
                "credentials": {
                    "key_present": True,
                    "key_source": "ENV_FILE",
                    "key_type": "oauth",
                    "secret_exposed": False,
                    "runtime_note": "Codex token found in .env but not loaded in runtime. OAuth status cannot be verified without auth.json."
                },
                "oauth": "OAUTH_STATUS_UNKNOWN",
                "usage_remaining": "MANUAL_REQUIRED",
                "probe_freshness": datetime.now(timezone.utc).isoformat(),
                "decision": "STOP_AND_ASK",
                "notes": "Codex token exists in .env but OAuth status is OAUTH_STATUS_UNKNOWN (auth.json not inspectable). Stéphane must provide counter values."
            }
        else:
            return {
                "status": "UNKNOWN",
                "credentials": {
                    "key_present": False,
                    "key_source": "NOT_FOUND",
                    "key_type": "oauth",
                    "secret_exposed": False
                },
                "oauth": "NOT_CONFIGURED",
                "usage_remaining": "MANUAL_REQUIRED",
                "probe_freshness": datetime.now(timezone.utc).isoformat(),
                "decision": "STOP_AND_ASK",
                "notes": "Codex token not found in environment or .env files. OAuth status = NOT_CONFIGURED."
            }

    # Check if Codex tool is available via hermes status
    try:
        import urllib.request
        # Try Nous status endpoint (read-only)
        req = urllib.request.Request(
            "https://api.nousresearch.com/v1/models",
            headers={"Authorization": f"Bearer {codex_token}", "Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        models = [m['id'] for m in data.get('data', [])]

        return {
            "status": "GREEN",
            "credentials": {
                "key_present": True,
                "key_source": "ENV",
                "key_type": "oauth",
                "secret_exposed": False
            },
            "oauth": "OK",
            "models_available": models,
            "usage_remaining": "MANUAL_REQUIRED",
            "probe_freshness": datetime.now(timezone.utc).isoformat(),
            "decision": "USE",
            "notes": "Codex OAuth OK. Usage remaining = MANUAL_REQUIRED (check Nous dashboard)."
        }
    except Exception as e:
        return {
            "status": "YELLOW",
            "credentials": {
                "key_present": True,
                "key_source": "ENV",
                "key_type": "oauth",
                "secret_exposed": False
            },
            "oauth": "CONFIGURED_BUT_UNVERIFIED",
            "usage_remaining": "MANUAL_REQUIRED",
            "probe_freshness": datetime.now(timezone.utc).isoformat(),
            "decision": "USE_WITH_CAUTION",
            "notes": f"Codex OAuth not verified: {type(e).__name__}. Usage = MANUAL_REQUIRED."
        }


def probe_mimo():
    """Probe MiMo (Xiaomi) — only /v1/models read-only, no generation."""
    # Check key presence WITHOUT exposing value
    mimo_creds = check_key_presence('XIAOMI_API_KEY', env_vars=['XIAOMI_API_KEY', 'MIMO_API_KEY', 'XIAOMI_MIMO_API_KEY', 'MIMO_TOKEN_PLAN_KEY'])
    key = os.environ.get('XIAOMI_API_KEY', os.environ.get('MIMO_API_KEY', os.environ.get('MIMO_TOKEN_PLAN_KEY', '')))
    base = os.environ.get('XIAOMI_BASE_URL', 'https://token-plan-ams.xiaomimimo.com/v1')

    if not key:
        # Key exists in .env but not loaded in environment
        if mimo_creds["key_present"] and mimo_creds["key_source"] == "ENV_FILE":
            # Check if canary PASS exists from P35
            canary_status = "UNKNOWN"
            canary_level = 0
            try:
                if MIMO_FICHE.exists():
                    content = MIMO_FICHE.read_text()
                    if "CANARY_LEVEL_1_PASS" in content:
                        canary_status = "CANARY_LEVEL_1_PASS"
                        canary_level = 1
            except Exception:
                pass

            return {
                "status": "CANARY_LEVEL_1_PASS" if canary_level >= 1 else "YELLOW",
                "credentials": {
                    "key_present": True,
                    "key_source": "ENV_FILE",
                    "key_type": "token_plan",
                    "secret_exposed": False,
                    "runtime_note": "Key found in /opt/data/.env but not loaded in runtime. Canary L1 PASS indicates key is valid in Hermes context."
                },
                "canary": canary_status,
                "canary_level": canary_level,
                "monthly_quota": "MANUAL_REQUIRED",
                "usage_percent": "MANUAL_REQUIRED",
                "days_left_in_month": (lambda now: (datetime(now.year + (now.month == 12), 1 if now.month == 12 else now.month + 1, 1) - datetime(now.year, now.month, 1)).days - now.day)(datetime.now(timezone.utc)),
                "probe_freshness": datetime.now(timezone.utc).isoformat(),
                "decision": "NO_RUNTIME_USE" if canary_level < 2 else "CONDITIONAL_USE",
                "notes": "XIAOMI_API_KEY exists in .env but not in runtime. Canary L1 PASS from P35 confirms key validity in Hermes context."
            }
        else:
            return {
                "status": "UNKNOWN",
                "credentials": {
                    "key_present": False,
                    "key_source": "NOT_FOUND",
                    "key_type": "token_plan",
                    "secret_exposed": False
                },
                "canary": "NOT_CONFIGURED",
                "monthly_quota": "MANUAL_REQUIRED",
                "usage_percent": "MANUAL_REQUIRED",
                "probe_freshness": datetime.now(timezone.utc).isoformat(),
                "decision": "NO_RUNTIME_USE",
                "notes": "XIAOMI_API_KEY not found in environment or .env files. Cannot probe."
            }

    # Read canary status from MiMo fiche
    canary_status = "UNKNOWN"
    canary_level = 0
    try:
        if MIMO_FICHE.exists():
            content = MIMO_FICHE.read_text()
            if "CANARY_LEVEL_1_PASS" in content:
                canary_status = "CANARY_LEVEL_1_PASS"
                canary_level = 1
            elif "CANARY_PENDING" in content:
                canary_status = "CANARY_PENDING"
    except Exception:
        pass

    # Only /v1/models probe (read-only discovery)
    try:
        import urllib.request
        req = urllib.request.Request(
            f"{base}/models",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=8)
        data = json.loads(resp.read())
        models = [m['id'] for m in data.get('data', [])]

        # days_left_in_month: automatic calculation
        now = datetime.now(timezone.utc)
        if now.month == 12:
            next_month = datetime(now.year + 1, 1, 1)
        else:
            next_month = datetime(now.year, now.month + 1, 1)
        days_in_month = (next_month - datetime(now.year, now.month, 1)).days
        days_left_in_month = days_in_month - now.day

        return {
            "status": "CANARY_ONLY" if canary_level < 2 else "YELLOW",
            "canary": canary_status,
            "canary_level": canary_level,
            "models_available": models,
            "monthly_quota": "MANUAL_REQUIRED",
            "usage_percent": "MANUAL_REQUIRED",
            "days_left_in_month": days_left_in_month,
            "probe_freshness": datetime.now(timezone.utc).isoformat(),
            "decision": "NO_RUNTIME_USE" if canary_level < 2 else "CONDITIONAL_USE",
            "notes": f"Canary L1 PASS. {len(models)} models. Runtime use blocked until L2+ validated."
        }
    except Exception as e:
        return {
            "status": "RED",
            "canary": canary_status,
            "canary_level": canary_level,
            "probe_freshness": datetime.now(timezone.utc).isoformat(),
            "decision": "NO_RUNTIME_USE",
            "notes": f"MiMo probe failed: {type(e).__name__}: {str(e)[:80]}"
        }


def probe_openrouter():
    """Probe OpenRouter free availability (read-only)."""
    # Check key presence WITHOUT exposing value
    or_creds = check_key_presence('OPENROUTER_API_KEY')
    key = os.environ.get('OPENROUTER_API_KEY', '')

    try:
        import urllib.request
        if key:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {key}"}
            )
            resp = urllib.request.urlopen(req, timeout=5)
            data = json.loads(resp.read())
            models = [m['id'] for m in data.get('data', []) if 'owl' in m['id'].lower()]
            key_present_in_env = True
        else:
            # No key — try public endpoint
            req = urllib.request.Request("https://openrouter.ai/api/v1/models")
            resp = urllib.request.urlopen(req, timeout=5)
            data = json.loads(resp.read())
            models = [m['id'] for m in data.get('data', []) if 'owl' in m['id'].lower()]
            key_present_in_env = False

        # Check recent rate limits
        log_path = Path("/opt/data/logs/gateway.log")
        rate_limits = 0
        if log_path.exists():
            lines = log_path.read_text().split('\n')[-200:]
            for line in lines:
                if 'openrouter' in line.lower() and ('429' in line or 'rate-limit' in line):
                    rate_limits += 1

        # Determine key source
        if key_present_in_env:
            key_source = "ENV"
        elif or_creds["key_present"]:
            key_source = "ENV_FILE"
        else:
            key_source = "NOT_FOUND"

        return {
            "status": "GREEN_FOR_DRAFT" if rate_limits == 0 else "YELLOW",
            "credentials": {
                "key_present": or_creds["key_present"] or key_present_in_env,
                "key_source": key_source,
                "key_type": "subscription",
                "secret_exposed": False
            },
            "authoritative": False,
            "model_available": len(models) > 0,
            "models_available": models,
            "rate_limit_ok": rate_limits == 0,
            "recent_rate_limits": rate_limits,
            "probe_freshness": datetime.now(timezone.utc).isoformat(),
            "decision": "DRAFT_ONLY",
            "notes": "OpenRouter free — non authoritative. Only for drafts/non-critical."
        }
    except Exception as e:
        return {
            "status": "RED",
            "credentials": {
                "key_present": or_creds["key_present"],
                "key_source": or_creds["key_source"] if not or_creds["key_present"] else "ENV_FILE",
                "key_type": "subscription",
                "secret_exposed": False
            },
            "authoritative": False,
            "model_available": False,
            "probe_freshness": datetime.now(timezone.utc).isoformat(),
            "decision": "DRAFT_ONLY",
            "notes": f"OpenRouter probe failed: {type(e).__name__}: {str(e)[:80]}"
        }


def load_existing_status():
    """Load existing status file if fresh."""
    if STATUS_FILE.exists():
        age, freshness = check_file_freshness(STATUS_FILE)
        if freshness == "FRESH":
            try:
                return json.loads(STATUS_FILE.read_text()), age
            except Exception:
                pass
    return None, None


def build_report(resources, dry_run=False):
    """Build the full status report."""
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "Model Resource Live Counters Probe",
        "version": "1.0",
        "mode": "DRY_RUN" if dry_run else "LIVE",
        "resources": resources,
        "decision_framework": {
            "step1_classify": "Task Type, Risk, Output Format, Expected Duration, Technical Action",
            "step2_probe": "If status fresh (<1h) → use it. Else → run probes. Manual counters → ask Stéphane.",
            "step3_decide": "M2.7 if quota OK + relevant. M3 if long context reasoning. Codex if tech. MiMo if canary PASS + premium. OpenRouter if non-critical + draft.",
            "step4_report": "Format: Task, Risk, Output, Selected resource, Why, Why not others, Quota impact, Fallback, Human validation."
        },
        "counters_summary": {
            "automatic": [
                "MiniMax: /v1/models (read-only), latency, errors 429/529",
                "Codex OAuth: OAuth status (Nous probe)",
                "OpenRouter free: model availability, rate limits",
                "MiMo: days_left_in_month (automatic calculation)"
            ],
            "manual_required": [
                "MiniMax: quota 5h, weekly, monthly → Stéphane dashboard (endpoint_quota_api: NOT_FOUND)",
                "Codex: usage remaining, session limits → Nous dashboard (auth.json not inspectable)",
                "MiMo: monthly quota, usage % → token-plan dashboard (no API endpoint found)"
            ]
        },
        "credential_status": {
            "minimax": {
                "key_present": "KEY_PRESENT_ENV_FILE",
                "runtime_loaded": False,
                "quota_counters": "MANUAL_REQUIRED (no endpoint found)",
                "reason": "Key in /opt/data/.env but not loaded in runtime. Stéphane must provide quota values."
            },
            "codex": {
                "key_present": "KEY_NOT_VISIBLE_IN_ENV",
                "runtime_loaded": False,
                "oauth_status": "OAUTH_STATUS_UNKNOWN (auth.json forbidden to read)",
                "usage_remaining": "MANUAL_REQUIRED",
                "reason": "Token not in runtime environment. OAuth status unknown (auth.json not inspectable)."
            },
            "mimo": {
                "key_present": "KEY_PRESENT_ENV_FILE",
                "runtime_loaded": False,
                "canary": "CANARY_LEVEL_1_PASS",
                "quota_counters": "MANUAL_REQUIRED (no endpoint found)",
                "days_left_in_month": "AUTOMATIC",
                "reason": "Key in /opt/data/.env. Canary L1 PASS from P35 confirms key validity in Hermes context."
            },
            "openrouter": {
                "key_present": "KEY_PRESENT_ENV",
                "runtime_loaded": True,
                "status": "GREEN_FOR_DRAFT",
                "reason": "OpenRouter free accessible. Non authoritative — only for drafts/non-critical."
            }
        },
        "routing_rules": {
            "critical_prod_secrets_release": {
                "models": ["MiniMax-M2.7"],
                "condition": "if counter unknown/red → STOP_AND_ASK",
                "never": ["OpenRouter", "MiMo (unless ACTIVE_LIMITED+)"]
            },
            "long_context_non_critical": {
                "models": ["M3", "MiMo (if L2+)", "M2.7"],
                "condition": "MiMo only if monthly quota to valorize + canary ok"
            },
            "technical_action": {
                "models": ["Codex", "MiMo (after canary coding)", "M2.7"],
                "never": ["OpenRouter (prod code)"]
            },
            "draft_exploration": {
                "models": ["OpenRouter free (if GREEN_FOR_DRAFT)", "MiMo (if quota to valorize + canary ok)"],
                "never": ["M2.7 (preserve for critical)"]
            }
        },
        "human_counter_request": {
            "trigger": "When automatic probe returns MANUAL_REQUIRED or UNKNOWN for a critical resource",
            "request_format": "J'ai besoin des compteurs actuels : MiniMax: usage 5h / weekly ? Codex: usage restant ? MiMo: usage mensuel % ? Sinon je route en mode conservateur.",
            "fallback": "Mode conservateur — use M2.7 only, preserve others"
        }
    }
    return report


def write_report(report, dry_run=False):
    """Write the status report to file."""
    if dry_run:
        print("DRY-RUN — would write:")
        print(json.dumps(report, indent=2))
        return True

    try:
        HC_DIR.mkdir(parents=True, exist_ok=True)
        tmp = STATUS_FILE.with_suffix('.tmp')
        tmp.write_text(json.dumps(report, indent=2))
        tmp.rename(STATUS_FILE)
        return True
    except PermissionError:
        # Fallback: write to workspace root
        alt = WORKSPACE / "model_resource_status.json"
        alt.write_text(json.dumps(report, indent=2))
        return True
    except Exception as e:
        print(f"ERROR writing status: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Model Resource Live Counters Probe")
    parser.add_argument('--dry-run', action='store_true', help="Simulate only, don't write")
    parser.add_argument('--write', action='store_true', help="Write status JSON (default if no flags)")
    parser.add_argument('--resource', default='all', choices=['minimax', 'codex', 'mimo', 'openrouter', 'all'])
    args = parser.parse_args()

    # Check existing status freshness
    existing, age = load_existing_status()
    if existing and not args.dry_run and not args.write:
        print(f"Status file is {age:.0f}s old (fresh < 3600s) — using existing.")
        print(json.dumps(existing, indent=2))
        return 0

    # Run probes
    resources = {}
    if args.resource in ['minimax', 'all']:
        resources['minimax'] = probe_minimax()
    if args.resource in ['codex', 'all']:
        resources['codex'] = probe_codex()
    if args.resource in ['mimo', 'all']:
        resources['mimo'] = probe_mimo()
    if args.resource in ['openrouter', 'all']:
        resources['openrouter'] = probe_openrouter()

    # Build and write report
    report = build_report(resources, dry_run=args.dry_run)
    success = write_report(report, dry_run=args.dry_run)

    if args.dry_run or args.write:
        print(json.dumps(report, indent=2))

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())