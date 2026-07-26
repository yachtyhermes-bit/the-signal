#!/usr/bin/env python3
import json, subprocess

slugs = [
    "asml-euv-monopoly-chokepoint-ai-chips",
    "credo-ai-connectivity-chips-2026",
    "smci-ai-server-accounting-comeback-2026",
    "vertiv-ai-data-center-infrastructure-q1-2026",
    "coinbase-european-crypto-moat-2026",
    "coreweave-ai-cloud-sale-2026",
    "kratos-defense-unmanned-systems-hypersonics-2026",
    "axon-ai-policing-monopoly-2026",
    "applied-materials-ai-chip-equipment-monopoly-2026",
    "servicenow-ai-workflow-automation-2026",
    "eaton-ai-power-infrastructure-monopoly-2026",
    "servicenow-ai-agent-enterprise-automation-2026",
    "crowdstrike-cybersecurity-ai-platform-2026",
    "alphabet-google-ai-multi-front-strategy-2026",
    "zscaler-zero-trust-cloud-security-2026",
    "leonardo-drs-defense-electronics-backbone-2026",
    "sofi-fintech-superapp-bank-charter-2026",
    "amd-mi400-datacenter-gpu-comeback-2026",
    "rocket-lab-neutron-reusability-2026",
    "tesla-fsd-robotaxi-ai-autonomy-2026",
    "aipo-ai-power-infra-dip-buy-june-2026",
    "ackman-microsoft-ai-bet",
    "ai-inversion-white-collar-blue-collar",
]

for slug in slugs:
    try:
        result = subprocess.run(
            ["curl", "-s", f"https://readthesignal.net/api/comments/?article={slug}"],
            capture_output=True, text=True, timeout=10
        )
        data = json.loads(result.stdout)
        comments = data.get("comments", data) if isinstance(data, dict) else data
        count = len(comments) if isinstance(comments, list) else -1
        print(f"{slug}: {count} comments")
    except Exception as e:
        print(f"{slug}: ERROR - {e}")
