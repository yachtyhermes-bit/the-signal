#!/usr/bin/env bash
# Deploy the built dist/ to the-signal Vercel project (pitfall 108: pin project.json
# explicitly so `vercel --prod` from dist/ cannot spawn a new dist-* project).
set -euo pipefail
cd /home/chino/thesignal/dist
rm -rf .vercel
mkdir -p .vercel
cat > .vercel/project.json <<'JSON'
{
  "projectId": "prj_injzyv7DMJ348G6KnMlHkz19i2U7",
  "orgId": "team_OPjTgGGvOQnlMiwxxnxJyMG7",
  "projectName": "the-signal"
}
JSON
npx vercel --prod --yes --archive=tgz
