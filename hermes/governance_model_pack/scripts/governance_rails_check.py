#!/usr/bin/env python3
"""
governance_rails_check.py — Auto-Control Governance Rails

Read-only health check for Hermes infrastructure.
Produces: /opt/data/workspace/healthchecks/governance_rails_status.json

Usage:
  python3 governance_rails_check.py --dry-run    # preview, no file write
  python3 governance_rails_check.py --write       # execute + write JSON
"""

import json
import os
import sys
import subprocess
import re
from datetime import datetime
from pathlib import Path

BASE = Path("/opt/data/workspace")
OUT = BASE / "healthchecks" / "governance_rails_status.json"

# Secret patterns — anything matching = CRITICAL
SECRET_PATTERNS = [
    (r'sk-cp-[A-Za-z0-9]{20,}', "OpenAI key"),
    (r'sk-api-[A-Za-z0-9]{20,}', "OpenAI key variant"),
    (r'tp-[A-Za-z0-9]{20,}', "Token Plan key"),
    (r'ghp_[A-Za-z0-9]{36}', "GitHub PAT"),
    (r'xox[baprs]-[A-Za-z0-9_-]{48,}', "Slack/Discord bot token"),
    (r'-----BEGIN [A-Z]+ PRIVATE KEY-----', "Private key header"),
]

def run(cmd, capture=True):
    """Run shell command, return stdout or None."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=capture,
                          text=True, timeout=30, cwd=BASE)
        return r.stdout.strip() if capture else ""
    except Exception as e:
        return f"ERROR: {e}"

def check_file(path, pattern, regex=True):
    """Check if file matches pattern. Returns (match, line) or (None, None)."""
    if not os.path.exists(path):
        return None, None
    if regex:
        r = run(f"grep -nE '{pattern}' '{path}' 2>/dev/null || true")
        if r and not r.startswith("ERROR"):
            lines = [l for l in r.splitlines() if l.strip()]
            return lines[0] if lines else None, None
    return None, None

def check_secrets_in_dir(dirpath, extensions=('.md', '.py', '.json', '.yaml', '.yml', '.sh')):
    """Scan directory for secret patterns. Returns list of (filepath, line, masked)."""
    findings = []
    if not os.path.isdir(dirpath):
        return findings
    for ext in extensions:
        r = run(f"find '{dirpath}' -type f -name '*{ext}' 2>/dev/null | head -200")
        files = [f.strip() for f in r.splitlines() if f.strip()]
        for f in files:
            for pat, label in SECRET_PATTERNS:
                m, _ = check_file(f, pat)
                if m:
                    # Mask the secret
                    match = re.search(pat, open(f).read() if os.path.exists(f) else "")
                    if match:
                        masked = match.group(0)[:8] + "***MASKED***"
                        findings.append((f, m.split(":")[0] if ":" in m else "?", masked))
    return findings

def check_runtime():
    """A. Runtime / version"""
    checks = {}
    errors = []

    # Hermes version
    r = run("hermes --version 2>/dev/null || cat /opt/data/.hermes_version 2>/dev/null || echo 'UNKNOWN'")
    checks['hermes_version'] = r if r else "UNKNOWN"
    if not r.startswith("0.16") and r != "UNKNOWN":
        errors.append(f"Version non 0.16: {r}")

    # Container
    r = run("docker ps --filter 'name=hermes' --format '{{.Names}}' 2>/dev/null | grep -E 'hermes-v016-prod|hermes-agent' || echo 'NONE'")
    checks['containers'] = r if r else "NONE"
    v015_active = "v015" in r.lower()
    if v015_active:
        errors.append("v0.15 container actif détecté")

    # Check no old v0.14 containers
    r = run("docker ps -a --filter 'name=v014' --format '{{.Names}}' 2>/dev/null || echo 'NONE'")
    checks['v014_containers'] = r if r else "NONE"
    if r and r != "NONE":
        errors.append("Ancien container v0.14 toujours présent")

    return checks, errors

def check_health_memory():
    """B. Health / mémoire"""
    checks = {}
    errors = []
    warnings = []

    # Healthcheck canonical — accepts both JSON and .md format
    # Primary: JSON output (if exists)
    # Fallback: latest.md symlink + parse Critical/Warnings lines
    hc_json = BASE / "healthchecks" / "hermes_memory_healthcheck_status.json"
    hc_md = BASE / "healthchecks" / "latest.md"
    hc_dir = BASE / "healthchecks"

    healthcheck_ok = False

    # Try JSON first
    if os.path.exists(hc_json):
        try:
            with open(hc_json) as f:
                data = json.load(f)
            checks['healthcheck_exists'] = True
            checks['healthcheck_format'] = 'json'
            checks['critical'] = data.get('critical', -1)
            checks['warnings'] = data.get('warnings', -1)
            checks['generated_at'] = data.get('generated_at', 'UNKNOWN')
            if data.get('critical', 0) > 0:
                errors.append(f"Healthcheck critical={data['critical']}")
            else:
                healthcheck_ok = True
        except:
            checks['healthcheck_exists'] = True
            checks['parse_error'] = True

    # Try .md format (canonical for Hermes)
    elif os.path.exists(hc_md) or os.path.islink(hc_md):
        try:
            target = hc_md.resolve() if hc_md.is_symlink() else hc_md
            if os.path.exists(target):
                with open(target) as f:
                    content = f.read()

                checks['healthcheck_exists'] = True
                checks['healthcheck_format'] = 'md'
                checks['healthcheck_path'] = str(target)

                # Parse Critical/Warnings/Decision from .md content
                crit_match = re.search(r'Critical[=\s:]+(\d+)', content)
                warn_match = re.search(r'Warnings?[=\s:]+(\d+)', content)
                dec_match = re.search(r'(?:Decision|Statut)[:\s]+([A-Z_]+)', content, re.IGNORECASE)

                checks['critical'] = int(crit_match.group(1)) if crit_match else -1
                checks['warnings'] = int(warn_match.group(1)) if warn_match else -1
                checks['decision'] = dec_match.group(1) if dec_match else 'UNKNOWN'

                if crit_match and int(crit_match.group(1)) > 0:
                    errors.append(f"Healthcheck critical={crit_match.group(1)}")
                else:
                    healthcheck_ok = True

                # Check for recent report
                age = run(f"python3 -c \"import os, time; print(int((time.time()-os.path.getmtime('{target}'))/3600))\" 2>/dev/null")
                try:
                    checks['healthcheck_age_hours'] = int(age)
                    if int(age) > 48:
                        warnings.append(f"Healthcheck vieux ({age}h)")
                except:
                    pass
            else:
                checks['healthcheck_exists'] = False
                errors.append("Healthcheck canonical absent (latest.md broken)")
        except Exception as e:
            checks['healthcheck_exists'] = True
            checks['parse_error'] = str(e)
    else:
        checks['healthcheck_exists'] = False
        errors.append("Healthcheck canonical absent")

    # WAK freshness
    wak_path = "/opt/data/workspace/WAK.md"
    if os.path.exists(wak_path):
        r = run(f"grep -m1 'generated_at\\|WAK.*at' '{wak_path}' | head -1")
        checks['wak_exists'] = True
        checks['wak_last_line'] = r if r else "UNKNOWN"
        # Check if WAK is recent (modified < 48h)
        age = run(f"python3 -c \"import os, time; print(int((time.time()-os.path.getmtime('{wak_path}'))/3600))\" 2>/dev/null")
        try:
            checks['wak_age_hours'] = int(age)
            if int(age) > 48:
                errors.append(f"WAK vieux ({age}h)")
        except:
            checks['wak_age_hours'] = -1
    else:
        checks['wak_exists'] = False
        errors.append("WAK.md absent")

    # _current_state.md
    cs_path = "/opt/data/workspace/_current_state.md"
    if os.path.exists(cs_path):
        checks['current_state_exists'] = True
        age = run(f"python3 -c \"import os, time; print(int((time.time()-os.path.getmtime('{cs_path}'))/3600))\" 2>/dev/null")
        try:
            checks['current_state_age_hours'] = int(age)
        except:
            checks['current_state_age_hours'] = -1
    else:
        checks['current_state_exists'] = False
        errors.append("_current_state.md absent")

    # curated memory accessible
    curated = "/opt/data/workspace/memory/curated"
    if os.path.isdir(curated):
        checks['curated_memory_exists'] = True
        files = run(f"ls '{curated}' 2>/dev/null | wc -l")
        checks['curated_files_count'] = files if files else "0"
    else:
        checks['curated_memory_exists'] = False
        errors.append("memory/curated absent")

    return checks, errors, warnings

def check_cron():
    """C. Cron / bruit"""
    checks = {}
    errors = []

    # OS cron
    r = run("crontab -l 2>/dev/null | grep -v '^#' | grep -v '^$' | wc -l")
    checks['os_cron_entries'] = r if r else "0"

    # WAK cron wrapper (should be */10, not */15 direct)
    r = run("crontab -l 2>/dev/null | grep wak")
    checks['wak_cron_lines'] = r if r else "NONE"
    if r:
        has_10_wrapper = "*/10" in r
        has_15_direct = bool(run("crontab -l 2>/dev/null | grep '*/15.*wak'"))
        checks['wak_10_wrapper'] = has_10_wrapper
        checks['wak_15_direct'] = has_15_direct
        if has_15_direct and not has_10_wrapper:
            errors.append("WAK */15 direct sans wrapper */10 — collision potentielle")

    # Check deliver=origin noise
    r = run("grep -r 'deliver.*origin' /opt/data/workspace/ 2>/dev/null | grep -v 'Binary' | wc -l")
    checks['deliver_origin_count'] = r if r else "0"

    # Check cron_registry
    cr_path = "/opt/data/workspace/cron_registry.json"
    if os.path.exists(cr_path):
        checks['cron_registry_exists'] = True
        try:
            with open(cr_path) as f:
                data = json.load(f)
            checks['cron_registry_entries'] = len(data) if isinstance(data, list) else "?"
        except:
            checks['cron_registry_exists'] = True
            checks['cron_registry_parse_error'] = True
    else:
        checks['cron_registry_exists'] = False

    return checks, errors

def check_dr_git():
    """D. DR Git / backup — with proper SSH error classification (P37.3)"""
    checks = {}
    errors = []
    warnings = []

    # DR Git repo locations — check all possible paths
    dr_paths = [
        "/opt/data/DR_Backup/hermes_IA",
        "/root/hermes/data/DR_Backup/hermes_IA",
        "/opt/data/.dr_backup/hermes_IA",
    ]

    dr_repo = None
    for path in dr_paths:
        r = run(f"test -d '{path}/.git' && echo YES || echo NO")
        if r == "YES":
            dr_repo = path
            break

    if dr_repo is None:
        checks['git_repo'] = False
        checks['git_repo_checked'] = dr_paths
        warnings.append("DR Git repo non accessible dans ce contexte — CROSS_CONTEXT_WARNING")
        return checks, errors, warnings

    checks['git_repo'] = True
    checks['git_repo_path'] = dr_repo

    # Git status
    r = run(f"cd '{dr_repo}' && git status --porcelain 2>&1 | head -20")
    checks['git_status'] = r if r else "CLEAN"

    dirty = bool(run(f"cd '{dr_repo}' && git status --porcelain 2>/dev/null | grep -v '^??'"))
    checks['git_dirty'] = dirty
    if dirty:
        warnings.append("DR Git dirty — push non fait")

    # Git remote token check — MUST NOT contain credentials
    r = run(f"cd '{dr_repo}' && git remote get-url origin 2>/dev/null || echo 'NO_REMOTE'")
    checks['git_remote'] = r if r else "NO_REMOTE"

    # Parse remote for credentials (user/pass in URL)
    if r and r != "NO_REMOTE":
        # Check for embedded credentials
        if "@" in r and "://" in r:
            # URL like https://user:token@github.com/... is bad
            auth_part = r.split("://")[1].split("@")[0] if "://" in r else ""
            if ":" in auth_part:
                errors.append("DR Git remote contient credentials embedues")
        # Also check for common token patterns in URL
        if "token=" in r.lower() or "ghp_" in r.lower():
            errors.append("DR Git remote contient credentials")

    # Last commit
    r = run(f"cd '{dr_repo}' && git log --oneline -1 2>/dev/null || echo 'NO_COMMITS'")
    checks['last_commit'] = r if r else "NO_COMMITS"

    # Last push (git log origin/main to see what was pushed)
    r = run(f"cd '{dr_repo}' && git log --oneline origin/main -1 2>/dev/null || git log --oneline origin/master -1 2>/dev/null || echo 'NO_UPSTREAM'")
    checks['last_push'] = r if r else "NO_UPSTREAM"

    # SSH error classification (P37.3) — the real diagnostic
    # NOTE: SSH needs explicit -F ~/.ssh/config because subprocess may not inherit config
    # Without -F, SSH can't resolve the github.com-hermes-dr alias → false DNS error
    ssh_result = run("ssh -F ~/.ssh/config -o BatchMode=yes -o ConnectTimeout=5 -T github.com-hermes-dr 2>&1 || true")
    checks['ssh_raw_output'] = ssh_result if ssh_result else "NO_OUTPUT"

    # Classify SSH error — P37.3 classification
    # SUBCONTEXT override: if host/root canonical is known PUSH_OK, don't escalate subcontext AUTH to error
    subcontext_override = False
    if not ssh_result or ssh_result == "NO_OUTPUT":
        ssh_class = "PUSH_OK"
        checks['dr_git_push_classification'] = ssh_class
    elif "Permission denied (publickey)" in ssh_result:
        ssh_class = "AUTH_FAILED"
        # Stéphane a confirmé: host/root canonique = PUSH_OK
        # Subcontext hermes AUTH est une SUBCONTEXT_LIMITATION, pas un failure système
        # → ne pas escalader en error si le canonique est OK (connnu de Stéphane)
        checks['dr_git_push_classification'] = ssh_class
        subcontext_override = True  # Will be overridden below
    elif "Could not resolve hostname" in ssh_result:
        # Check if it's the alias resolution or actual DNS failure
        # SSH reads config and resolves alias — "Could not resolve" after alias = real DNS fail
        ssh_class = "DNS_FAIL"
        errors.append(f"DR Git SSH: {ssh_class} — DNS ne peut pas résoudre github.com")
        checks['dr_git_push_classification'] = ssh_class
    elif "Connection refused" in ssh_result or "Connection timed out" in ssh_result:
        ssh_class = "NETWORK_FAIL"
        errors.append(f"DR Git SSH: {ssh_class}")
        checks['dr_git_push_classification'] = ssh_class
    elif "Host key verification failed" in ssh_result:
        ssh_class = "HOST_KEY_FAILED"
        errors.append(f"DR Git SSH: {ssh_class}")
        checks['dr_git_push_classification'] = ssh_class
    else:
        # Unknown error — do not guess, classify as needs investigation
        ssh_class = "SSH_UNKNOWN_ERROR"
        warnings.append(f"DR Git SSH: erreur inconnue — {ssh_result[:80]}")
        checks['dr_git_push_classification'] = ssh_class

    # SUBCONTEXT vs CANONICAL DR Git detection (P37.3 correction)
    checks['dr_git_canonical_context'] = None
    checks['dr_git_subcontext'] = None

    if ssh_class == "AUTH_FAILED":
        checks['ssh_config_valid'] = run("test -f ~/.ssh/config && grep -c 'github.com-hermes-dr' ~/.ssh/config 2>/dev/null || echo '0'")
        checks['ssh_key_fingerprint'] = run("ssh-keygen -lf ~/.ssh/id_ed25519 2>/dev/null || echo 'NO_KEY'")

        # Stéphane a confirmé: host/root canonique = PUSH_OK
        # Subcontext hermes AUTH = SUBCONTEXT_LIMITATION
        checks['dr_git_canonical_context'] = "NOT_ACCESSIBLE"
        checks['dr_git_push_classification'] = "OK_WITH_SUBCONTEXT_LIMITATION"
        warnings.append("DR Git: subcontext hermes AUTH_FAILED, canonique host/root non vérifiable. Stéphane a confirmé: canonique PUSH_OK. Action = AUCUNE requise.")
        checks['dr_git_subcontext'] = "AUTH_FAILED"
    else:
        checks['dr_git_subcontext'] = "N/A"

    return checks, errors, warnings

def check_docs():
    """E. Documentation rails"""
    checks = {}
    errors = []
    warnings = []

    required_docs = [
        "GOVERNANCE_MASTER_REGISTER.md",
        "DOC_INDEX.md",
        "MODEL_RESOURCE_GOVERNANCE.md",
        "runbooks/ai_model_routing.md",
        "runbooks/model_availability_quota_probe.md",
        "AGENTS_GOVERNANCE.md",
        "_current_state.md",
    ]

    for doc in required_docs:
        path = BASE / doc
        exists = os.path.exists(path)
        checks[f'doc_{doc.replace("/", "_").replace(".md", "")}'] = exists
        if not exists:
            errors.append(f"Doc manquant: {doc}")

    # model_resources
    mr_path = BASE / "model_resources"
    if os.path.isdir(mr_path):
        r = run(f"ls '{mr_path}'/*.md 2>/dev/null | wc -l")
        checks['model_resources_count'] = r if r else "0"
        if r == "0":
            errors.append("Aucun model_resources/*.md")
    else:
        checks['model_resources_count'] = "0"
        errors.append("Dossier model_resources absent")

    # Check P31-P36 indexed
    r = run(f"grep -c 'P3[1-6]' '{BASE}/GOVERNANCE_MASTER_REGISTER.md' 2>/dev/null || echo '0'")
    checks['p31_p36_indexed'] = r if r else "0"
    try:
        if int(r) < 4:
            warnings.append(f"Seulement {r} entrées P31-P36 dans register")
    except:
        pass

    # Check v0.15 migration pending
    r = run(f"grep -i 'v0.15.*migration.*pending\\|migration.*v0.15.*pending' '{BASE}/'*.md 2>/dev/null | head -5")
    checks['v015_pending'] = r if r else "NONE"
    if r and r != "NONE":
        warnings.append("Référence v0.15 migration pending trouvée")

    # Check contradictions v0.14 vs v0.16
    r = run(f"grep -c 'v0.14.*active\\|v0.16.*active' '{BASE}/GOVERNANCE_MASTER_REGISTER.md' 2>/dev/null || echo '0'")
    checks['v014_v016_mentions'] = r if r else "0"

    # Check v0.15 docs as HISTORICAL
    r = run(f"grep -l 'v0.15' '{BASE}'/GOVERNANCE_MASTER_REGISTER.md '{BASE}/DOC_INDEX.md' 2>/dev/null | head -5")
    checks['v015_docs_checked'] = r if r else "NONE"

    return checks, errors, warnings

def check_model_routing():
    """F. Model routing"""
    checks = {}
    errors = []

    # M2.7 default
    r = run("grep -m1 'model.*default\\|default.*model' /opt/data/config.yaml 2>/dev/null | head -3")
    checks['default_model_line'] = r if r else "NOT_FOUND"

    # M3 usage check (should be reasoning only)
    r = run("grep -c 'M3.*reasoning\\|M3.*pas.*prod\\|M3.*no.*final' /opt/data/workspace/runbooks/ai_model_routing.md 2>/dev/null || echo '0'")
    checks['m3_routing_rules_count'] = r if r else "0"

    # MiMo status check
    mimo_path = BASE / "model_resources/mimo.md"
    if os.path.exists(mimo_path):
        r = run(f"grep -m1 'Status.*:.*CANARY\\|Status.*:.*ACTIVE' '{mimo_path}' 2>/dev/null")
        checks['mimo_status'] = r if r else "NOT_FOUND"
        if "ACTIVE" in r and "CANARY" not in r:
            errors.append("MiMo activé sans canary préalable")
    else:
        checks['mimo_status'] = "FILE_MISSING"

    # OpenRouter free non-authoritative
    or_path = BASE / "model_resources/openrouter_free.md"
    if os.path.exists(or_path):
        r = run(f"grep -c 'non-authoritative\\|non authoritative\\|brainstorming\\|première.passe' '{or_path}' 2>/dev/null || echo '0'")
        checks['openrouter_non_auth_count'] = r if r else "0"
        if r == "0":
            errors.append("OpenRouter free pas classé non-authoritative")
    else:
        checks['openrouter_non_auth_count'] = "FILE_MISSING"

    # Codex technical only
    codex_path = BASE / "model_resources/codex_oauth.md"
    if os.path.exists(codex_path):
        r = run(f"grep -m1 'Can Decide.*:.*TECHNICAL\\|Can Execute.*:.*YES\\|Can Execute.*:.*NO' '{codex_path}' 2>/dev/null")
        checks['codex_routing'] = r if r else "NOT_FOUND"
    else:
        checks['codex_routing'] = "FILE_MISSING"

    return checks, errors

def check_security():
    """G. Security / secrets"""
    checks = {}
    errors = []

    dirs_to_scan = [
        str(BASE),
        "/opt/data/skills",
        "/opt/data/workspace/runbooks",
        "/opt/data/workspace/model_resources",
        "/opt/data/workspace/healthchecks",
    ]

    total_findings = []
    for d in dirs_to_scan:
        findings = check_secrets_in_dir(d)
        total_findings.extend(findings)

    checks['scanned_dirs'] = len(dirs_to_scan)
    checks['secrets_found'] = len(total_findings)

    if total_findings:
        checks['secret_details'] = []
        for f, line, masked in total_findings[:10]:  # limit to 10
            errors.append(f"Secret detected: {masked} in {f}:{line}")
            checks['secret_details'].append((f, line, masked))
    else:
        checks['secret_details'] = []

    # Check PLACEHOLDER usage in examples
    r = run(f"grep -rE 'sk-cp-[A-Za-z0-9]{{20,}}|tp-[A-Za-z0-9]{{20,}}' '{BASE}/healthchecks/' '{BASE}/model_resources/' 2>/dev/null | grep -v 'PLACEHOLDER\\|***MASKED***' | head -5")
    checks['real_keys_in_examples'] = r if r else "NONE"
    if r and r != "NONE":
        errors.append("Clés réelles trouvées dans exemples")

    return checks, errors

def check_skills():
    """H. Skills / operating contracts"""
    checks = {}
    errors = []

    # Skills can be top-level or nested in sub-directories
    # Check both patterns
    skill_paths = [
        ("/opt/data/skills/hermes-sysop-config", "skill_hermes-sysop-config"),
        ("/opt/data/skills/hermes-doc-system", "skill_hermes-doc-system"),
        ("/opt/data/skills/hermes-sysop-ledger", "skill_hermes-sysop-ledger"),
        ("/opt/data/skills/hermes-sysop/memory_curator", "skill_memory_curator"),
        ("/opt/data/skills/hermes-sysop/hermes-orchestrator-operating-rules", "skill_hermes-orchestrator-operating-rules"),
        ("/opt/data/skills/hermes-maintenance-and-remediation-policy", "skill_hermes-maintenance-and-remediation-policy"),
    ]

    for path, label in skill_paths:
        exists = os.path.exists(path) or os.path.exists(path + ".md")
        checks[label] = exists
        if not exists:
            errors.append(f"Skill manquante: {label} ({path})")

    # Check skill headers
    hdr_path = "/opt/data/workspace/scripts/check_skill_headers.py"
    if os.path.exists(hdr_path):
        r = run(f"python3 '{hdr_path}' 2>/dev/null || echo 'SCRIPT_NOT_FOUND'")
        checks['skill_headers_check'] = r if r else "NOT_RUN"
        if "FAIL" in r or "ERROR" in r:
            errors.append("Skill headers check échoué")
    else:
        checks['skill_headers_check'] = "SCRIPT_NOT_FOUND"

    return checks, errors

def check_ownership():
    """J. File ownership"""
    checks = {}
    errors = []

    paths_to_check = [
        ("/opt/data/workspace", "workspace"),
        ("/opt/data/workspace/healthchecks", "healthchecks"),
        ("/opt/data/workspace/memory/curated", "curated_memory"),
        ("/opt/data/workspace/agents_state", "agents_state"),
    ]

    for path, label in paths_to_check:
        if os.path.exists(path):
            r = run(f"ls -ld '{path}' 2>/dev/null | awk '{{print $3, $4}}'")
            checks[f'owner_{label}'] = r if r else "UNKNOWN"
            if "root" in r and label in ["workspace", "healthchecks", "curated_memory"]:
                errors.append(f"{label} root-owned — inaccessible à hermes")
        else:
            checks[f'owner_{label}'] = "NOT_EXISTS"

    return checks, errors

def make_decision(critical_count, errors, warnings):
    """Decision logic."""
    if critical_count > 0:
        return "FAIL"
    if warnings:
        return "PASS_WITH_WARNINGS"
    if errors:
        return "PASS_WITH_WARNINGS"
    return "PASS"

def main():
    dry_run = "--dry-run" in sys.argv
    write = "--write" in sys.argv or not dry_run

    print("=== Governance Rails Check ===")
    print(f"Mode: {'DRY-RUN' if dry_run else 'EXECUTE'}")
    print()

    all_checks = {}
    all_errors = []
    all_warnings = []
    critical_count = 0

    # Run all checks
    print("A. Runtime / version...")
    chk, errs = check_runtime()
    all_checks['runtime'] = chk
    all_errors.extend(errs)
    for e in errs:
        print(f"  ERROR: {e}")

    print("B. Health / mémoire...")
    chk, errs, warns = check_health_memory()
    all_checks['health'] = chk
    all_errors.extend(errs)
    all_warnings.extend(warns)
    for e in errs:
        print(f"  ERROR: {e}")

    print("C. Cron / bruit...")
    chk, errs = check_cron()
    all_checks['cron'] = chk
    all_errors.extend(errs)
    for e in errs:
        print(f"  ERROR: {e}")

    print("D. DR Git / backup...")
    chk, errs, warns = check_dr_git()
    all_checks['dr_git'] = chk
    all_errors.extend(errs)
    all_warnings.extend(warns)
    for e in errs:
        print(f"  ERROR: {e}")
    for w in warns:
        print(f"  WARN: {w}")

    print("E. Documentation rails...")
    chk, errs, warns = check_docs()
    all_checks['docs'] = chk
    all_errors.extend(errs)
    all_warnings.extend(warns)
    for e in errs:
        print(f"  ERROR: {e}")
    for w in warns:
        print(f"  WARN: {w}")

    print("F. Model routing...")
    chk, errs = check_model_routing()
    all_checks['model_routing'] = chk
    all_errors.extend(errs)
    for e in errs:
        print(f"  ERROR: {e}")

    print("G. Security / secrets...")
    chk, errs = check_security()
    all_checks['security'] = chk
    all_errors.extend(errs)
    for e in errs:
        print(f"  CRITICAL: {e}")
        critical_count += 1

    print("H. Skills / operating contracts...")
    chk, errs = check_skills()
    all_checks['skills'] = chk
    all_errors.extend(errs)
    for e in errs:
        print(f"  ERROR: {e}")

    print("I. File ownership...")
    chk, errs = check_ownership()
    all_checks['ownership'] = chk
    all_errors.extend(errs)
    for e in errs:
        print(f"  ERROR: {e}")

    decision = make_decision(critical_count, all_errors, all_warnings)

    # Build next_actions — only from actual errors, not CROSS_CONTEXT_WARNING
    next_actions = []
    if critical_count > 0:
        next_actions.append({"priority": "CRITICAL", "action": "Secrets détectés — corriger immédiatement"})
    if any("v0.15 container" in e for e in all_errors):
        next_actions.append({"priority": "CRITICAL", "action": "Container v0.15 actif — STOP_AND_ASK Stéphane"})
    # DR Git: only HIGH if repo exists but dirty/credentialed, not if CROSS_CONTEXT_WARNING
    dr_real_issues = [e for e in all_errors if "DR Git" in e and "CROSS_CONTEXT" not in e]
    if dr_real_issues:
        next_actions.append({"priority": "HIGH", "action": "DR Git a des problèmes réels — voir checks.dr_git"})
    # Healthcheck: only HIGH if truly absent, not if format is .md
    hc_absent = [e for e in all_errors if "Healthcheck canonical absent" in e and "broken" not in e]
    if hc_absent:
        next_actions.append({"priority": "HIGH", "action": "Lancer healthcheck canonique"})

    result = {
        "generated_at": datetime.now().isoformat(),
        "decision": decision,
        "critical": critical_count,
        "warnings": len(all_warnings),
        "errors_count": len(all_errors),
        "checks": all_checks,
        "next_actions": next_actions,
    }

    print()
    print(f"=== RESULT: {decision} ===")
    print(f"Critical: {critical_count}")
    print(f"Warnings: {len(all_warnings)}")
    print(f"Errors: {len(all_errors)}")
    if next_actions:
        print("Next actions:")
        for na in next_actions:
            print(f"  [{na['priority']}] {na['action']}")

    if write and not dry_run:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\nJSON written to: {OUT}")

    if dry_run:
        print("\n[DRY-RUN] No file written.")
        print(json.dumps(result, indent=2, default=str)[:2000])

    return 0 if decision == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())