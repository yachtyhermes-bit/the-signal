import requests

url = "https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/tsm-august-sales-ai-demand-2026.jpg"
r = requests.head(url, timeout=30, allow_redirects=True)
print("HTTP", r.status_code, "| content-type:", r.headers.get("content-type"), "| content-length:", r.headers.get("content-length"))
