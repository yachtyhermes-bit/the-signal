#!/usr/bin/env python3
"""Generate hero image via FAL.ai flux/schnell and search YouTube for video."""
import os
import sys
import json
import time
import requests
from urllib.parse import quote

FAL_API = "https://queue.fal.run"
RESULTS_API = "https://queue.fal.run"
FAL_KEY = os.environ["FAL_KEY"]
HEADERS = {"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"}
OUTPUT_PATH = "/home/chino/thesignal/public/img/articles/amazon-aws-ai-kuiper-dark-horse-2026.jpg"

PROMPT = (
    "Professional macro close-up photograph of a satellite communication laser link in space with "
    "Earth's curvature in background. A beam of light connecting two points above the atmosphere. "
    "Shallow depth of field, photorealistic, cinematic lighting. Dark space background with subtle "
    "blue planet glow. No people, no buildings, no text labels, no numbers, no markings."
)

def submit_image_generation():
    """Submit async job to FAL."""
    url = f"{FAL_API}/fal-ai/flux/schnell"
    payload = {
        "prompt": PROMPT,
        "image_size": {"width": 1344, "height": 768},
        "num_images": 1,
        "enable_safety_checker": False,
    }
    print(f"Submitting to {url} ...")
    r = requests.post(url, headers=HEADERS, json=payload, timeout=30)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(json.dumps(data, indent=2))
    return data

def poll_status(request_id):
    """Poll the status endpoint."""
    status_url = f"{FAL_API}/fal-ai/flux/schnell/requests/{request_id}/status"
    while True:
        r = requests.get(status_url, headers=HEADERS, timeout=30)
        data = r.json()
        status = data.get("status", "UNKNOWN")
        print(f"Status: {status}")
        if status == "COMPLETED":
            return data
        elif status in ("FAILED", "ERROR"):
            print(json.dumps(data, indent=2))
            return None
        time.sleep(2)

def get_result(request_id):
    """Get the result including image URLs."""
    result_url = f"{RESULTS_API}/fal-ai/flux/schnell/requests/{request_id}"
    r = requests.get(result_url, headers=HEADERS, timeout=30)
    data = r.json()
    print(json.dumps(data, indent=2))
    return data

def download_image(url, dest):
    """Download image from URL and save to dest."""
    print(f"Downloading image from {url} ...")
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(r.content)
    print(f"Saved to: {dest} ({len(r.content)} bytes)")

def try_sync_api():
    """Try the synchronous API directly."""
    url = f"https://fal.run/fal-ai/flux/schnell"
    payload = {
        "prompt": PROMPT,
        "image_size": {"width": 1344, "height": 768},
        "num_images": 1,
        "enable_safety_checker": False,
    }
    print(f"Trying sync API at {url} ...")
    r = requests.post(url, headers=HEADERS, json=payload, timeout=90)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(json.dumps(data, indent=2))
    return data

def search_youtube():
    """Search YouTube for Amazon Kuiper / AWS AI video via Google."""
    # Try YouTube Data API if key available, else use web search approach
    # Using the noembed service to search
    channels = ["CNBC", "Bloomberg", "Yahoo Finance"]
    query_base = "Amazon Kuiper AWS satellite"

    # Try to find a video via Google search-like approach
    # Using Invidious or YouTube embed search
    search_terms = [
        "Amazon Kuiper satellite CNBC 2025",
        "Amazon Kuiper satellite Bloomberg 2025",
        "Amazon AWS Kuiper Yahoo Finance 2025",
    ]

    print("\n=== YouTube Video Search ===")
    for term in search_terms:
        print(f"\nSearching: {term}")
        # Use YouTube's oembed to test a video URL - but we need to find one first
        # Let's try searching via a YouTube embed page
    return None

def verify_youtube_oembed(video_id):
    """Verify a video exists using YouTube's oembed endpoint."""
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    r = requests.get(url, timeout=15)
    if r.status_code == 200:
        data = r.json()
        print(f"oEmbed verified: {json.dumps(data, indent=2)}")
        return data
    else:
        print(f"oEmbed failed: {r.status_code}")
        return None


if __name__ == "__main__":
    # Step 1: Generate image via FAL
    print("=" * 60)
    print("STEP 1: Generate Hero Image via FAL.ai")
    print("=" * 60)

    # Try sync API first (simpler)
    try:
        result = try_sync_api()
        images = result.get("images", [])
        if images:
            image_url = images[0].get("url")
            if image_url:
                download_image(image_url, OUTPUT_PATH)
            else:
                print("No image URL in sync response")
        else:
            print("No images in sync response, trying async...")
            raise Exception("fallback to async")
    except Exception as e:
        print(f"Sync API failed: {e}")
        print("\nTrying async queue API...")
        try:
            submit_data = submit_image_generation()
            request_id = submit_data.get("request_id") or submit_data.get("id")
            if request_id:
                print(f"Request ID: {request_id}")
                poll_status(request_id)
                result = get_result(request_id)
                images = result.get("images", [])
                if images:
                    image_url = images[0].get("url")
                    if image_url:
                        download_image(image_url, OUTPUT_PATH)
                else:
                    print("No images in async result")
            else:
                print(f"No request_id in submit response: {submit_data}")
        except Exception as e2:
            print(f"Async API also failed: {e2}")
            import traceback
            traceback.print_exc()

    # Step 2: YouTube search
    print("\n" + "=" * 60)
    print("STEP 2: YouTube Video Search")
    print("=" * 60)

    # Known likely videos - search via oembed with candidate IDs
    # Let's try to use YouTube's search suggestions API or similar
    known_ids_to_try = [
        # We'll try the YouTube search suggestion endpoint
    ]

    # Use YouTube's oembed with a search
    # Actually let's use the YouTube Data API v3 search if key available, else try common approaches
    yt_key = os.environ.get("YOUTUBE_API_KEY", "")

    if yt_key:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": "Amazon Kuiper satellite",
            "channelId": "",
            "maxResults": 5,
            "order": "date",
            "key": yt_key,
        }
        # Search for each channel
        for channel in ["UCUpfy_Gad1bQ2THV68gQnow",  # CNBC
                        "UCIALMVvV6yBmV_BfDhQTRuw",  # Bloomberg Quicktake (example)
                        "UCrSoMM0jgC7qMh0b0n1E5uw"]: # Yahoo Finance (example)
            params["channelId"] = channel
            r = requests.get(url, params=params, timeout=15)
            if r.status_code == 200:
                data = r.json()
                items = data.get("items", [])
                if items:
                    vid = items[0]
                    vid_id = vid["id"]["videoId"]
                    title = vid["snippet"]["title"]
                    channel_title = vid["snippet"]["channelTitle"]
                    print(f"\nFound: {title}")
                    print(f"Channel: {channel_title}")
                    print(f"ID: {vid_id}")
                    oembed_data = verify_youtube_oembed(vid_id)
                    break
    else:
        print("No YOUTUBE_API_KEY - using oembed with candidate video IDs")
        print("Searching via YouTube web approach...")

        # Try well-known recent Kuiper videos via oembed verification
        # These are plausible IDs from recent coverage
        candidate_ids = [
            # Let me try a known format - search YouTube embed page
        ]

        # Use a simpler approach - try YouTube search via requests to suggest endpoint
        suggest_url = "https://suggestqueries.google.com/complete/search"
        params = {
            "client": "youtube",
            "ds": "yt",
            "q": "Amazon Kuiper CNBC 2025"
        }
        r = requests.get(suggest_url, params=params, timeout=10)
        print(f"Suggest response: {r.status_code}")
        if r.status_code == 200:
            print(r.text[:500])

    print("\n\nDone.")
