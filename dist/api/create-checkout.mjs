// Stripe Checkout — Vercel serverless function
// Creates a Stripe Checkout Session linked to a Hive account
// Accepts: { plan, token (hive auth token), email? (optional override) }

const SK = process.env.STRIPE_SECRET_KEY || '';
const ADMIN_KEY = process.env.ADMIN_KEY || '';

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
    const { plan, token, email: overrideEmail } = req.body || {};

    // Resolve Hive user from token
    let userUid = null;
    let userEmail = overrideEmail || '';
    let userDisplayName = '';

    if (token && token.startsWith('tok_')) {
      try {
        const meResp = await fetch(`https://readthesignal.net/api/hive?action=me&token=${encodeURIComponent(token)}`, {
          signal: AbortSignal.timeout(5000)
        });
        if (meResp.ok) {
          const meData = await meResp.json();
          if (meData.authenticated) {
            userUid = meData.uid;
            userEmail = meData.email || userEmail;
            userDisplayName = meData.displayName || '';
          }
        }
      } catch (err) {
        console.warn('Hive lookup failed:', err.message);
      }
    }

    // Build Stripe checkout params
    const params = new URLSearchParams();
    params.append('line_items[0][quantity]', '1');
    params.append('mode', 'subscription');
    params.append('success_url', `https://readthesignal.net/account?success=true&plan=${plan}`);
    params.append('cancel_url', 'https://readthesignal.net/pricing?canceled=true');
    params.append('allow_promotion_codes', 'true');
    params.append('billing_address_collection', 'auto');

    // Set the price based on plan (STRIPE_PREMIUM_PRICE_ID env var)
    const priceId = plan === 'pro'
      ? (process.env.STRIPE_PRO_PRICE_ID || '')
      : (process.env.STRIPE_PREMIUM_PRICE_ID || '');

    if (!priceId) {
      return res.status(400).json({ error: `Price ID not configured for plan "${plan}". Set STRIPE_PREMIUM_PRICE_ID or STRIPE_PRO_PRICE_ID.` });
    }
    params.append('line_items[0][price]', priceId);

    // Set customer email if available
    if (userEmail) {
      params.append('customer_email', userEmail);
    }

    // Pass Hive metadata so webhook can link back
    if (userUid) params.append('metadata[hive_uid]', userUid);
    params.append('metadata[plan]', plan || 'premium');
    if (userDisplayName) params.append('metadata[display_name]', userDisplayName);

    const stripeResp = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + SK,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: params.toString()
    });

    const session = await stripeResp.json();

    if (session.url) {
      return res.json({ url: session.url, sessionId: session.id });
    } else {
      console.error('Stripe error:', JSON.stringify(session).slice(0, 500));
      return res.status(500).json({ error: 'Could not create checkout session.' });
    }
  } catch (err) {
    console.error('Checkout error:', err);
    return res.status(500).json({ error: 'Something went wrong.' });
  }
}
