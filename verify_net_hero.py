"""Verify the NET hero image is live on R2 CDN."""
import requests

CDN = 'https://pub-4b6ad449790f433c8b0fde9b167147c9.r2.dev'
KEY = 'img/articles/net-earnings-beat-q2-2026.jpg'
url = CDN + '/' + KEY

r = requests.head(url, timeout=30)
print('HTTP', r.status_code)
print('Content-Type:', r.headers.get('Content-Type'))
print('Content-Length:', r.headers.get('Content-Length'))
print('URL:', url)
print('RESULT:', 'OK' if r.status_code == 200 else 'FAIL')
