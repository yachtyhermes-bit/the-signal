import requests
r = requests.get('https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev/img/articles/msft-azure-100b-2026.jpg', timeout=30)
print('CDN status:', r.status_code)
print('Content-Type:', r.headers.get('Content-Type'))
print('Bytes:', len(r.content))
