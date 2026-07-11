#!/usr/bin/env python3
import json, subprocess

slugs = [
    "broadcom-ai-networking-custom-chip-dominance-2026",
    "broadcom-ai-networking-vmware-dominance-2026",
    "marvell-ai-custom-chips-data-center-2026",
    "micron-ai-memory-hbm-dominance-2026",
    "nvidia-cuda-ai-moat-2026",
    "palantir-ai-platform-warfare-2026",
    "palantir-aip-commercial-expansion-2026",
    "signal-top-6-avgo-nvda-pltr-ceg-crwv-rtx",
    "l3harris-defense-avionics-contracts-2026",
    "kratos-defense-ai-dronewarfare-dominance-2026",
    "crowdstrike-ai-security-platform-2026",
    "alphabet-ai-cloud-waymo-undervalued-2026",
    "amazon-aws-ai-kuiper-dark-horse-2026",
    "applied-materials-other-chip-monopoly-2026",
    "asml-euv-lithography-monopoly-ai-chips-2026",
    "microsoft-azure-ai-copilot-enterprise-2026",
    "sofi-fintech-bank-charter-galileo-2026",
    "meta-ai-infrastructure-revenue-2026",
    "arista-ai-data-center-networking-2026",
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
