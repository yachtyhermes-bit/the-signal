// Stripe Checkout — Vercel serverless function
// Creates a Stripe Checkout Session and returns the URL

const SK = process.env.STRIPE_SECRET_KEY || '';
const PRICE_IDS = {
  premium: process.env.STRIPE_PREMIUM_PRICE_ID || 'price_premium_monthly',
  pro: process.env.STRIPE_PRO_PRICE_ID || 'price_pro_monthly'
};

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
    const { plan } = req.body || {};
    if (!plan || !PRICE_IDS[plan]) {
      return res.status(400).json({ error: 'Invalid plan selected.' });
    }

    const encoded = new URLSearchParams({
      'line_items[0][price]': PRICE_IDS[plan],
      'line_items[0][quantity]': '1',
      'mode': 'subscription',
      'success_url': 'https://readthesignal.net/pricing?success=true',
      'cancel_url': 'https://readthesignal.net/pricing?canceled=true',
      'allow_promotion_codes': 'true',
      'billing_address_collection': 'auto'
    });

    const stripeResp = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + SK,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: encoded
    });

    const session = await stripeResp.json();

    if (session.url) {
      return res.json({ url: session.url });
    } else {
      console.error('Stripe error:', session);
      return res.status(500).json({ error: 'Could not create checkout session.' });
    }
  } catch (err) {
    console.error('Checkout error:', err);
    return res.status(500).json({ error: 'Something went wrong.' });
  }
}
