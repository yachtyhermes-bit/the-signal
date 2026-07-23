import subprocess

# Investigate AMAT links
urls = [
    "https://investors.appliedmaterials.com/",
    "https://www.benzinga.com/quote/AMAT/analyst-ratings",
]

for url in urls:
    print(f"\n=== {url} ===")
    
    # Try with verbose curl
    result = subprocess.run(
        ['curl', '-sI', '-v', '-L', '--max-time', '15', '-A', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36', url],
        capture_output=True, text=True, timeout=20
    )
    print("HEADERS:")
    print(result.stdout[:1500])
    if result.stderr:
        print("STDERR:")
        print(result.stderr[:500])
    
    # Also try a full fetch for the Benzinga one
    if 'benzinga' in url:
        result2 = subprocess.run(
            ['curl', '-s', '-L', '--max-time', '10', '-A', 'Mozilla/5.0', url],
            capture_output=True, text=True, timeout=15
        )
        body_lower = result2.stdout.lower()
        if '404' in body_lower[:2000]:
            print("\nFull body snippet (first 2000 chars):")
            print(result2.stdout[:2000])
