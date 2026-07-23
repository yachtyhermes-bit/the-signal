import subprocess, json

slugs = [
    "snow-ai-data-cloud-consumption-2026",
    "amat-picks-shovels-ai-supercycle-2026", 
    "crm-agentforce-doubt-discount-2026",
    "rbrk-cyber-resilience-secular-growth-2026",
    "avav-counterdrone-switchblade-contracts-2026",
]

for slug in slugs:
    with open(f'articles/posts/{slug}.json') as f:
        a = json.load(f)
    
    links = a.get('links', [])
    print(f"\n=== {slug} ===")
    
    for li in links:
        url = li.get('url', '')
        label = li.get('label', '?')
        
        try:
            result = subprocess.run(
                ['curl', '-sI', '-L', '--max-time', '10', '-A', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', url],
                capture_output=True, text=True, timeout=15
            )
            output = result.stdout
            lines = output.split('\n')
            status_line = lines[0] if lines else 'NO RESPONSE'
            http_code = '???'
            if 'HTTP/' in status_line:
                parts = status_line.split(' ')
                http_code = parts[1] if len(parts) > 1 else '???'
            
            content_type = ''
            for line in lines:
                if 'content-type:' in line.lower():
                    content_type = line.strip()
            
            if http_code in ['200', '301', '302', '308']:
                if '404' in output:
                    print(f"  ⚠️ {label}: {url}")
                    print(f"    Status: {http_code} but contains 404 in response")
                else:
                    print(f"  ✅ {label}: {url}")
                    print(f"    Status: {http_code}, {content_type}")
            elif http_code in ['403', '429']:
                print(f"  ⚠️ (blocked) {label}: {url} — {http_code} (paywall/bot block, acceptable)")
            else:
                print(f"  ❌ {label}: {url}")
                print(f"    Status: {http_code}")
                if result.stderr:
                    print(f"    Error: {result.stderr[:100]}")
        except Exception as e:
            print(f"  ❌ {label}: {url}")
            print(f"    Exception: {e}")

print("\n=== LINK CHECK COMPLETE ===")
