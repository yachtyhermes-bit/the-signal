// Comments API — Vercel serverless function
// GET  /api/comments/?article=slug  → returns comments
// POST /api/comments/              → adds a comment (body: {article, text, author, parentId})

const COMMENTS_PATH = '/tmp/comments.json';

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
      const { article, text, author, photoURL, uid, parentId } = req.body || {};

      if (!article || !text || !author) {
        return res.status(400).json({ error: 'Missing required fields (article, text, author)' });
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
        uid: uid || null,
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
