#!/usr/bin/env python3
"""Final GET verification of MRVL hero image on R2 CDN."""
import requests

slug = 'mrvl-nvidia-nvlink-fusion-alliance-2026'
base1 = 'https://pub-b58d4c6c4d614e2fa6f8d786e09f27d1' + '.r2.dev'
base2 = 'https://pub-4b6ad449790f433c8b0fde9b167147c9' + '.r2.dev'
path = '/img/articles/' + slug + '.jpg'

for label, base in [('task-specified', base1), ('script-R2_CDN', base2)]:
    url = base + path
    try:
        r = requests.get(url, timeout=30)
        body = r.content
        print(label, 'HTTP', r.status_code, '| bytes:', len(body), '| type:', r.headers.get('content-type'))
        if r.status_code == 200 and body[:2] == b'\xff\xd8':
            print('  -> valid JPEG payload')
    except Exception as e:
        print(label, url, 'ERROR:', e)
