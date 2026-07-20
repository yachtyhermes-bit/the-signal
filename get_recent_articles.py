#!/usr/bin/env python3
import json
import os
from glob import glob
from datetime import datetime

articles_dir = "/home/chino/thesignal/articles/posts"
articles = []

for fpath in glob(os.path.join(articles_dir, "*.json")):
    try:
        with open(fpath) as f:
            data = json.load(f)
        # Extract date — try multiple fields
        date_val = data.get("date") or data.get("published_date") or data.get("pubDate")
        if date_val:
            # Parse different formats
            for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d", "%B %d, %Y"]:
                try:
                    dt = datetime.strptime(date_val, fmt)
                    break
                except ValueError:
                    continue
            else:
                continue
        else:
            continue
        articles.append((dt, fpath, data))
    except Exception as e:
        print(f"Error reading {fpath}: {e}")

# Sort newest first
articles.sort(key=lambda x: x[0], reverse=True)

for dt, fpath, data in articles[:8]:
    slug = os.path.splitext(os.path.basename(fpath))[0]
    title = data.get("title", "No title")
    print(f"{dt.date().isoformat()} | {slug} | {title}")
