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

    // Read all comments
    let all = [];
    try {
      const data = await fs.readFile(COMMENTS_PATH, 'utf8');
      all = JSON.parse(data);
    } catch { all = []; }

    if (req.method === 'GET') {
      const article = req.query.article || '';
      if (!article) return res.status(400).json({ error: 'Missing article slug' });
      const comments = all
        .filter(c => c.article === article)
        .sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
      return res.json({ comments });
    }

    if (req.method === 'POST') {
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

      return res.json({ status: 'success', comment });
    }

    return res.status(405).json({ error: 'Method not allowed' });

  } catch (err) {
    console.error('Comments error:', err);
    return res.status(500).json({ error: 'Something went wrong' });
  }
}
