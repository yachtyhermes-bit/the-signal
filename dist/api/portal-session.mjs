// Stripe Customer Portal — Vercel serverless function
// Creates a billing portal session so users can manage subscriptions
// (cancel, update payment method, view invoices, etc.)

const SK = process.env.STRIPE_SECRET_KEY || '';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  if (!SK) {
    return res.status(500).json({ error: 'Stripe not configured.' });
  }

  try {
    const { token } = req.body || {};
    if (!token) {
      return res.status(400).json({ error: 'Auth token required' });
    }

    // Resolve Hive user from token
    let userEmail = '';
    let stripeCustomerId = '';

    try {
      const meResp = await fetch(`https://readthesignal.net/api/hive?action=me&token=${encodeURIComponent(token)}`, {
        signal: AbortSignal.timeout(5000)
      });
      if (meResp.ok) {
        const meData = await meResp.json();
        if (meData.authenticated) {
          userEmail = meData.email || '';
          stripeCustomerId = meData.stripeCustomerId || '';
        }
      }
    } catch (err) {
      console.warn('Hive lookup failed:', err.message);
    }

    if (!stripeCustomerId) {
      return res.status(400).json({ error: 'No Stripe customer found. You must subscribe before accessing the billing portal.' });
    }

    // Create Stripe billing portal session
    const params = new URLSearchParams();
    params.append('customer', stripeCustomerId);
    params.append('return_url', 'https://readthesignal.net/account');

    const stripeResp = await fetch('https://api.stripe.com/v1/billing_portal/sessions', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + SK,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: params.toString()
    });

    const session = await stripeResp.json();

    if (session.url) {
      return res.json({ url: session.url });
    } else {
      console.error('Stripe portal error:', JSON.stringify(session).slice(0, 500));
      return res.status(500).json({ error: 'Could not create billing portal session.' });
    }
  } catch (err) {
    console.error('Portal session error:', err);
    return res.status(500).json({ error: 'Something went wrong.' });
  }
}
