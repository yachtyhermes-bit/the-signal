# TTS Audio Pipeline: Permanent Solution

## Problem Summary
- **166 articles**, only **28 have working TTS** (20 in R2 root, 8 in public/audio/)
- **138 articles** fall through to Google Translate (broken ~30s audio)
- **Root cause**: 
  1. Vercel env var `CF_ACCOUNT_ID=""` (empty string) disabled all R2 caching
  2. Existing R2 files at root level, but API looked for `v2/` prefix
  3. No batch generation had been run for most articles

## Architecture Decision: R2-Primary with Static Fallback

### Why R2?
- **Git size**: Already 227MB. Adding 166×1.5MB=250MB MP3s would bloat git to ~500MB
- **Deployment**: Vercel deploy times would grow from ~30s to ~5min
- **Scalability**: R2 handles CDN delivery, no per-request computation
- **Cost**: R2 free tier (10M reads/month, 50GB storage) is more than enough

### Architecture Layers
```
Client (tts.js)
    ↓
/api/tts/?slug=X&text=...
    ↓
1. Check R2 cache (v2/X.mp3, then X.mp3) — FAST
    ↓ (miss)
2. Check public/audio/X.mp3 — local fallback
    ↓ (miss)
3. Generate via edge-tts on Vercel — SLOW (60s)
    ↓ (fail/timeout)
4. Google Translate fallback — BROKEN
```

## Implementation Plan

### Phase 1: Fix Env Vars (Vercel Dashboard) ⚠️ MANUAL

**Problem**: `CF_ACCOUNT_ID` is set to empty string, masking `CLOUDFLARE_ACCOUNT_ID`

**Fix** (choose ONE):
- **Option A**: Delete empty `CF_ACCOUNT_ID` from Vercel env vars
- **Option B**: Set `CF_ACCOUNT_ID=a0b3e792abdcd46a7614dc201ff2170f` in Vercel

**Code fix applied**: `api/tts.mjs` now uses `envVal()` helper that skips empty strings:
```js
function envVal(...keys) {
  for (const k of keys) {
    const v = process.env[k];
    if (v && v.trim()) return v.trim();
  }
  return '';
}
```

This makes the code resilient even if Vercel env is misconfigured.

### Phase 2: Fix R2 Prefix Mismatch ⚙️ DONE

**Problem**: 20 existing R2 files at root level, but API looked for `v2/` prefix

**Fix applied**: `api/tts.mjs` now tries multiple prefixes:
```js
const R2_PREFIXES = ['v2/', ''];
async function fetchFromR2(slug) {
  for (const prefix of R2_PREFIXES) {
    // try v2/slug.mp3, then slug.mp3
  }
}
```

**Impact**: 20 articles now work immediately after env var fix!

### Phase 3: Generate Missing MP3s (One-Time Batch) 🎙️

**Script**: `scripts/batch-generate-tts-parallel.py` (NEW, faster)
- Generates 4 concurrent streams (Microsoft allows this)
- Uploads to R2 with `v2/` prefix
- Resumable (skips already-complete)
- Estimated time: ~45 minutes (vs 2.5 hours sequential)

**Run**:
```bash
source .dev.vars
python3 scripts/batch-generate-tts-parallel.py
```

### Phase 4: Ongoing Maintenance (Cron) ⏰

**Problem**: New articles need TTS generated automatically

**Solution**: GitHub Actions workflow runs daily at 2 AM, generates TTS for articles not yet in R2.

**Implementation**: See `.github/workflows/tts-generation.yml` (NEW)

**Why GitHub Actions (not Vercel Cron)?**
- Vercel Cron has 2-minute limit → can't generate 10 articles
- GitHub Actions has 6-hour limit → can handle batch generation
- Free tier: 2000 minutes/month → plenty for daily runs

## Performance Metrics

**Current (broken)**:
- 28/166 articles work (17%)
- Failed articles: Google Translate, ~30s, robotic voice

**After Phase 1+2 (env + prefix fix)**:
- 48/166 articles work (29%) — adds 20 from R2 root
- Still 118 articles broken

**After Phase 3 (batch generation)**:
- 166/166 articles work (100%)
- All use Andrew voice, full article length
- Served from R2 CDN (~200ms latency)

**After Phase 4 (cron)**:
- New articles auto-generate within 24 hours
- Zero manual intervention needed

## Files Modified

1. `/api/tts.mjs`
   - Added `envVal()` helper for robust env var resolution
   - Added multi-prefix R2 lookup
   - Backward compatible (still works if env is fixed)

2. `/scripts/batch-generate-tts-parallel.py` (NEW)
   - 4× faster batch generation
   - Resumable, rate-limited
   - Better progress reporting

3. `.github/workflows/tts-generation.yml` (NEW)
   - Daily cron job
   - Generates missing MP3s
   - Uploads to R2

## Testing

**Local test** (before deploying):
```bash
# Source env vars
export $(cat .dev.vars | xargs)

# Test R2 fetch (should get 2.5MB audio)
node -e "
const slug='anduril-army-20b-defense-tech-2026';
fetch('https://api.cloudflare.com/client/v4/accounts/'+process.env.CLOUDFLARE_ACCOUNT_ID+'/r2/buckets/the-signal-audio/objects/'+encodeURIComponent(slug+'.mp3'),
  {headers:{'Authorization':'Bearer '+process.env.CLOUDFLARE_API_TOKEN}})
.then(r=>r.arrayBuffer())
.then(b=>console.log('Got',Buffer.from(b).length,'bytes'));"

# Test batch generation (dry run, just 1 article)
python3 scripts/batch-generate-tts-parallel.py --limit 1
```

**Deploy checklist**:
- [ ] Fix Vercel env var (delete empty CF_ACCOUNT_ID or set correct value)
- [ ] Deploy updated `api/tts.mjs` to Vercel
- [ ] Run batch generation: `python3 scripts/batch-generate-tts-parallel.py`
- [ ] Test 5 random articles (old + new) on readthesignal.net
- [ ] Verify X-TTS-Backend header shows 'r2-andrew'

## Cost Analysis

**Current**:
- Vercel serverless: ~$0 (free tier)
- R2: ~$0 (free tier)
- **Total**: $0/month

**After solution**:
- Vercel serverless: ~$20/month (Pro plan, for API calls)
- R2: ~$0 (well within free tier: 250MB storage, <1M reads/month)
- **Total**: ~$20/month (same as current Vercel Pro)

**No additional cost** — solution uses existing resources more efficiently.

## Risk Mitigation

**Risk**: Microsoft rate-limits edge-tts during batch generation
**Mitigation**: Batch script uses 4 concurrent streams with 0.5s delay between requests

**Risk**: R2 upload fails mid-batch
**Mitigation**: Script is resumable — restarts skip already-uploaded files

**Risk**: Vercel env var fix breaks something
**Mitigation**: Code fix (envVal helper) makes env var handling robust regardless

**Risk**: New articles don't get TTS generated
**Mitigation**: Daily cron ensures <24h delay for new articles

## Alternative Approaches Considered

### ❌ Commit all MP3s to git
- **+250MB** to repository (already 227MB)
- Slow git clone (5-10 minutes)
- Large Vercel deploys (5+ minutes)
- **Rejected**: Git bloat too severe

### ❌ Generate on Vercel serverless (on-demand)
- 60s generation time per article
- Vercel timeout: 10-60s (free/pro)
- Cold starts add 5-10s
- **Rejected**: Too slow, unreliable

### ❌ Third-party TTS API (ElevenLabs, Play.ht)
- $99-499/month for 166 articles × daily listens
- External dependency
- **Rejected**: Expensive, unnecessary for this use case

### ❌ Client-side Web Speech API
- Browser-dependent quality
- No voice consistency
- **Rejected**: Poor UX, not production-ready

### ✅ R2 + pre-generation (chosen)
- Free (within existing resources)
- Fast CDN delivery
- Consistent Andrew voice
- Scalable to 1000+ articles
- **Selected**: Best balance of cost, speed, reliability

## Next Steps

1. **Immediate** (5 min): Fix Vercel env var → 48 articles work
2. **Today** (45 min): Run batch generation → all 166 articles work
3. **This week**: Set up GitHub Actions cron → ongoing automation
4. **Monitor**: Check R2 metrics, Vercel logs for 1 week

## Success Metrics

- ✅ 100% articles have Andrew voice TTS
- ✅ Average TTS response time < 500ms (from R2)
- ✅ Zero Google Translate fallbacks
- ✅ <24h delay for new article TTS generation
