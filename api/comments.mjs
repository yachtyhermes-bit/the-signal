// Comments API — Vercel serverless function
// Only authenticated users can post (Google or The Hive)
// GET  /api/comments/?article=slug  → returns comments
// POST /api/comments/              → adds a comment (requires auth)

import crypto from 'crypto';

const COMMENTS_PATH = '/tmp/comments.json';
const HIVE_SECRET = 'hive_signal_secret_2026_' + (process.env.HIVE_SECRET || 'default_dev_secret');
const HIVE_API = 'https://readthesignal.net/api/hive';

// Service token for AI comment blasts — bypasses auth
const SERVICE_TOKEN = process.env.COMMENT_SERVICE_TOKEN || 'hive-comment-blast-2026';

// GitHub persistence — prevent data loss on Vercel cold starts
const GITHUB_TOKEN = process.env.GITHUB_TOKEN || '';
const GITHUB_OWNER = 'yachtyhermes-bit';
const GITHUB_REPO = 'the-signal';
const GITHUB_PATH = 'data/comments.json';
const GITHUB_BRANCH = 'main';

async function loadFromGitHub() {
  if (!GITHUB_TOKEN) return [];
  try {
    const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${GITHUB_PATH}?ref=${GITHUB_BRANCH}`;
    const resp = await fetch(url, {
      headers: { 'Authorization': `token ${GITHUB_TOKEN}` },
      signal: AbortSignal.timeout(5000)
    });
    if (!resp.ok) return [];
    const fileInfo = await resp.json();
    const content = Buffer.from(fileInfo.content, 'base64').toString('utf8');
    return JSON.parse(content);
  } catch { return []; }
}

async function saveToGitHub(all) {
  if (!GITHUB_TOKEN) return;
  try {
    const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${GITHUB_PATH}`;
    const content = Buffer.from(JSON.stringify(all, null, 2)).toString('base64');
    
    let sha = null;
    try {
      const getResp = await fetch(url, {
        headers: { 'Authorization': `token ${GITHUB_TOKEN}` },
        signal: AbortSignal.timeout(5000)
      });
      if (getResp.ok) {
        const fileInfo = await getResp.json();
        sha = fileInfo.sha;
      }
    } catch {}
    
    const body = { message: 'Update comments', content, branch: GITHUB_BRANCH };
    if (sha) body.sha = sha;
    
    await fetch(url, {
      method: 'PUT',
      headers: { 'Authorization': `token ${GITHUB_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(10000)
    });
  } catch (err) { console.error('GitHub comments save failed:', err.message); }
}

function verifyHiveToken(token) {
  if (!token || typeof token !== 'string') return null;
  if (!token.startsWith('tok_')) return null;
  const rest = token.slice(4);
  const parts = rest.split('.');
  if (parts.length !== 3) return null;
  const [b64User, b64Expires, sig] = parts;
  const payload = b64User + '.' + b64Expires;
  const expectedSig = crypto.createHmac('sha256', HIVE_SECRET).update(payload).digest('hex').slice(0, 24);
  if (sig !== expectedSig) return null;
  const username = Buffer.from(b64User, 'base64url').toString();
  const expiresAt = parseInt(Buffer.from(b64Expires, 'base64url').toString(), 10);
  if (Date.now() > expiresAt) return null;
  return username;
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();

  try {
    const fs = await import('fs/promises');

    // Read all comments — try /tmp first, fall back to GitHub
    let all = [];
    try {
      const data = await fs.readFile(COMMENTS_PATH, 'utf8');
      all = JSON.parse(data);
    } catch {
      // /tmp empty (cold start) — load from GitHub
      all = await loadFromGitHub();
      if (all.length > 0) {
        try { await fs.writeFile(COMMENTS_PATH, JSON.stringify(all, null, 2), 'utf8'); } catch {}
      }
    }

    if (req.method === 'GET') {
      const article = req.query.article || '';
      const action = req.query.action || '';
      
      // GET /api/comments?action=likes&commentId=XXX → get like count
      if (action === 'likes' && req.query.commentId) {
        const comment = all.find(c => c.id === req.query.commentId);
        if (!comment) return res.status(404).json({ error: 'Comment not found' });
        return res.json({ commentId: comment.id, likes: (comment.likes || []).length, likedBy: comment.likes || [] });
      }
      
      if (!article) return res.status(400).json({ error: 'Missing article slug' });
      const comments = all
        .filter(c => c.article === article)
        .sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
      return res.json({ comments });
    }

    if (req.method === 'POST') {
       // POST /api/comments?action=like → toggle like on a comment
      if (req.query.action === 'like') {
        const { commentId, uid, token } = req.body || {};
        if (!commentId) return res.status(400).json({ error: 'Missing commentId' });
        const hiveToken = token || req.query.token;
        const isServiceCall = (hiveToken === SERVICE_TOKEN);
        const likerId = isServiceCall ? (uid || 'swarm-' + Math.random().toString(36).slice(2,6)) : (uid || hiveToken);
        if (!likerId && !isServiceCall) return res.status(401).json({ error: 'Auth required' });
        
        const comment = all.find(c => c.id === commentId);
        if (!comment) return res.status(404).json({ error: 'Comment not found' });
        
        if (!comment.likes) comment.likes = [];
        const idx = comment.likes.indexOf(likerId);
        if (idx >= 0) {
          comment.likes.splice(idx, 1); // unlike
        } else {
          comment.likes.push(likerId); // like
        }
        
        await fs.writeFile(COMMENTS_PATH, JSON.stringify(all, null, 2), 'utf8');
        saveToGitHub(all).catch(() => {});
        return res.json({ status: 'success', liked: idx < 0, likeCount: comment.likes.length });
      }

      const { article, text, author, photoURL, uid, parentId, token } = req.body || {};

      if (!article || !text || !author) {
        return res.status(400).json({ error: 'Missing required fields (article, text, author)' });
      }

      // Verify authentication
      const hiveToken = token || req.query.token;
      const isServiceCall = (hiveToken === SERVICE_TOKEN);
      const hiveUsername = (!isServiceCall && hiveToken) ? verifyHiveToken(hiveToken) : null;

      if (!isServiceCall && !hiveUsername && !uid) {
        return res.status(401).json({ error: 'Authentication required. Sign in with Google or The Hive to comment.' });
      }

      // For Hive auth, verify user exists
      if (hiveUsername) {
        try {
          const verifyResp = await fetch(HIVE_API + '?action=me&token=' + encodeURIComponent(hiveToken), {
            signal: AbortSignal.timeout(5000)
          });
          const verifyData = await verifyResp.json();
          if (!verifyData.authenticated) {
            return res.status(401).json({ error: 'Session expired. Please sign in again.' });
          }
        } catch {
          // If hive API is unreachable, accept the token we already verified locally
          // (stateless verification passed, so it's valid)
        }
      }

      // Validate parentId if provided
      if (parentId) {
        const parentExists = all.some(c => c.id === parentId && c.article === article);
        if (!parentExists) {
          return res.status(400).json({ error: 'Parent comment not found' });
        }
      }

      const clean = text.trim();
      if (clean.length < 1) return res.status(400).json({ error: 'Comment is empty' });
      if (clean.length > 2000) return res.status(400).json({ error: 'Comment too long (max 2000)' });

      const comment = {
        id: Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 8),
        article,
        text: clean,
        author: author.trim().slice(0, 50),
        photoURL: photoURL || null,
        uid: uid || hiveUsername || null,
        parentId: parentId || null,
        createdAt: new Date().toISOString()
      };

      all.push(comment);
      await fs.writeFile(COMMENTS_PATH, JSON.stringify(all, null, 2), 'utf8');
      saveToGitHub(all).catch(() => {}); // fire-and-forget persist

      return res.json({ status: 'success', comment });
    }

    return res.status(405).json({ error: 'Method not allowed' });

  } catch (err) {
    console.error('Comments error:', err);
    return res.status(500).json({ error: 'Something went wrong' });
  }
}
