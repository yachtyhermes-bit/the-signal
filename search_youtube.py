#!/usr/bin/env python3
"""Search YouTube for Amazon Kuiper videos and verify with oembed."""
import os
import requests
import json
import re

YOUTUBE_OEMBED = "https://www.youtube.com/oembed"

def verify_video(video_id):
    """Verify video exists via oembed."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        r = requests.get(YOUTUBE_OEMBED, params={"url": url, "format": "json"}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return {
                "id": video_id,
                "url": url,
                "title": data.get("title"),
                "channel": data.get("author_name"),
                "verified": True
            }
    except Exception as e:
        pass
    return None

def search_via_web(query):
    """Try to extract video IDs from YouTube search results HTML."""
    from urllib.parse import quote
    search_url = f"https://www.youtube.com/results?search_query={quote(query)}"
    try:
        r = requests.get(search_url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        })
        if r.status_code == 200:
            # Extract video IDs from the HTML
            video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', r.text)
            return video_ids[:10]  # First 10 unique IDs
    except Exception as e:
        print(f"Web search failed: {e}")
    return []

def main():
    print("Searching for Amazon Kuiper videos on YouTube...")
    
    # Search queries targeting major channels
    queries = [
        "Amazon Kuiper CNBC",
        "Amazon Kuiper Bloomberg",
        "Amazon Kuiper Yahoo Finance",
        "AWS Kuiper satellite",
        "Amazon satellite internet 2025"
    ]
    
    found_videos = []
    
    for query in queries:
        print(f"\nSearching: {query}")
        video_ids = search_via_web(query)
        
        if video_ids:
            print(f"Found {len(video_ids)} video IDs")
            # Try to verify each video
            for vid_id in video_ids[:5]:  # Check first 5
                result = verify_video(vid_id)
                if result and result["verified"]:
                    print(f"✓ Verified: {result['title']}")
                    print(f"  Channel: {result['channel']}")
                    print(f"  URL: {result['url']}")
                    
                    # Check if it's from a target channel
                    channel_lower = result["channel"].lower()
                    if any(target in channel_lower for target in ["cnbc", "bloomberg", "yahoo"]):
                        found_videos.append(result)
                        print(f"  ★ Target channel found!")
                    else:
                        found_videos.append(result)
                    
                    if len(found_videos) >= 3:  # Found enough
                        break
            else:
                continue
            break
    
    if found_videos:
        print("\n" + "="*60)
        print("TOP RESULTS:")
        print("="*60)
        best = found_videos[0]
        print(f"\nBest match:")
        print(f"  Title: {best['title']}")
        print(f"  Channel: {best['channel']}")
        print(f"  Video ID: {best['id']}")
        print(f"  URL: {best['url']}")
        
        # Save to JSON for the parent agent
        with open("/tmp/youtube_result.json", "w") as f:
            json.dump(best, f, indent=2)
        
        return best
    else:
        print("\nNo videos found from target channels")
        return None

if __name__ == "__main__":
    result = main()
    sys_exit = 0 if result else 1
