#!/usr/bin/env python3
"""
check-video-duration.py — YouTube video duration checker for The Signal

Usage:
    python3 scripts/check-video-duration.py VIDEO_ID
    python3 scripts/check-video-duration.py dQw4w9WgXcQ

Returns:
    exit 0: OK (duration 2-20 min)
    exit 1: REJECT (too short <2 min or too long >20 min)
    exit 2: WARN (could not determine, check manually)

Requirements: stdlib only (urllib, json, re)
"""

import urllib.request, json, sys, re

MAX_SECONDS = 1200  # 20 minutes
MIN_SECONDS = 120   # 2 minutes

def get_duration(video_id):
    """Fetch YouTube watch page and extract duration."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        return None, None, f"HTTP error: {e}"

    # Extract title
    title_match = re.search(r'<title>([^<]+)', html)
    title = title_match.group(1).replace(' - YouTube', '').strip() if title_match else video_id

    # Method 1: ytInitialPlayerResponse JSON
    m = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});', html, re.DOTALL)
    if m:
        try:
            data = json.loads(m.group(1))
            dur_str = data.get('videoDetails', {}).get('lengthSeconds')
            if dur_str:
                return int(dur_str), title, None
        except (json.JSONDecodeError, ValueError):
            pass

    # Method 2: ISO 8601 duration from meta tag
    m = re.search(r'itemprop="duration"\s+content="([^"]+)"', html)
    if m:
        iso = m.group(1)
        hours = re.search(r'(\d+)H', iso)
        minutes = re.search(r'(\d+)M', iso)
        seconds = re.search(r'(\d+)S', iso)
        h = int(hours.group(1)) if hours else 0
        m_val = int(minutes.group(1)) if minutes else 0
        s = int(seconds.group(1)) if seconds else 0
        return h * 3600 + m_val * 60 + s, title, None

    return None, title, "Could not parse duration from page"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} VIDEO_ID")
        sys.exit(2)

    video_id = sys.argv[1].strip()
    duration, title, error = get_duration(video_id)

    if error:
        print(f"WARN: {error} for video '{video_id}' ('{title}') — verify manually")
        sys.exit(2)

    mins = duration // 60
    secs = duration % 60

    if duration > MAX_SECONDS:
        print(f"REJECT: Video '{title}' is {mins}m{secs}s ({mins} min) — exceeds 20 min max")
        sys.exit(1)
    elif duration < MIN_SECONDS:
        print(f"REJECT: Video '{title}' is only {mins}m{secs}s — needs at least 2 min")
        sys.exit(1)
    else:
        print(f"OK: Video '{title}' is {mins}m{secs}s ✅")
        sys.exit(0)
