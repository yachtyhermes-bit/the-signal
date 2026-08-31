// Activate Premium after Stripe Checkout — Vercel serverless function
// Verifies the Stripe Checkout Session completed and upgrades the user
// POST: { session_id, token (hive auth token) }

const SK = process.env.STRIPE_SECRET_KEY || '';
const ADMIN_KEY = process.env.ADMIN_KEY || '';
const HIVE_API = 'https://readthesignal.net/api/hive';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  if (!SK) {
    return res.status(500).json({ error: 'Stripe not configured. Add STRIPE_SECRET_KEY to Vercel env vars.' });
  }

  try {
    const { session_id, token } = req.body || {};

    if (!session_id) {
      return res.status(400).json({ error: 'Missing session_id' });
    }

    // Resolve Hive user from token
    let username = '';
    let userUid = '';
    let userEmail = '';

    if (token && token.startsWith('tok_')) {
      try {
        const meResp = await fetch(`${HIVE_API}?action=me&token=${encodeURIComponent(token)}`, {
          signal: AbortSignal.timeout(5000)
        });
        if (meResp.ok) {
          const meData = await meResp.json();
          if (meData.authenticated) {
            userUid = meData.uid;
            username = meData.username || '';
            userEmail = meData.email || '';
          }
        }
      } catch (err) {
        console.warn('Hive lookup failed:', err.message);
      }
    }

    if (!username && !userUid) {
      return res.status(401).json({ error: 'Could not verify user identity. Please sign in again.' });
    }

    // Verify the Stripe session
    const stripeResp = await fetch(`https://api.stripe.com/v1/checkout/sessions/${session_id}`, {
      headers: {
        'Authorization': 'Bearer ' + SK
      }
    });

    if (!stripeResp.ok) {
      const errText = await stripeResp.text();
      console.error('Stripe session lookup failed:', errText.slice(0, 200));
      return res.status(500).json({ error: 'Could not verify payment session.' });
    }

    const session = await stripeResp.json();

    // Check session is paid/completed
    if (session.payment_status !== 'paid' && session.payment_status !== 'no_payment_required') {
      return res.status(400).json({ error: 'Payment not completed yet.', status: session.payment_status });
    }

    if (session.status !== 'complete') {
      return res.status(400).json({ error: 'Checkout session not complete.', status: session.status });
    }

    // Determine plan from session
    const plan = session.metadata?.plan || 'premium';

    if (!ADMIN_KEY) {
      return res.status(500).json({ error: 'ADMIN_KEY not configured' });
    }

    // Activate premium via Hive API (POST admin endpoint — same path the webhook uses)
    const activateResp = await fetch(
      `${HIVE_API}?action=set-premium&admin_key=${encodeURIComponent(ADMIN_KEY)}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          admin_key: ADMIN_KEY,
          email: userEmail || username,
          plan,
          hiveUid: userUid
        }),
        signal: AbortSignal.timeout(10000)
      }
    );

    const result = await activateResp.json();

    if (!activateResp.ok) {
      console.error('set-premium failed:', result);
      return res.status(500).json({ error: 'Failed to activate premium. Contact support.' });
    }

    console.log(`Premium activated for ${username} (plan: ${plan}) via session ${session_id}`);

    return res.json({
      success: true,
      username: username,
      plan: plan,
      message: `You are now a ${plan} member!`
    });

  } catch (err) {
    console.error('Activation error:', err);
    return res.status(500).json({ error: 'Something went wrong.' });
  }
}
