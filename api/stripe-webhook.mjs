// Stripe Webhook — Vercel serverless function
// Handles: checkout.session.completed, customer.subscription.deleted
// Persists premium status via Hive API (set-premium / cancel-premium actions)

const SK = process.env.STRIPE_SECRET_KEY || '';
const WH_SECRET = process.env.STRIPE_WEBHOOK_SECRET || '';
const ADMIN_KEY = process.env.ADMIN_KEY || '';
const HIVE_API = 'https://readthesignal.net/api/hive';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  if (!ADMIN_KEY) {
    console.log('Webhook: ADMIN_KEY not configured');
    return res.status(500).json({ error: 'ADMIN_KEY not configured' });
  }

  try {
    // Parse the event
    let event;
    if (WH_SECRET && req.headers['stripe-signature']) {
      // Verify signature
      const stripe = await import('stripe');
      const stripeClient = new stripe.default(SK);
      const sig = req.headers['stripe-signature'];
      // Get raw body for verification
      const rawBody = typeof req.body === 'string' ? req.body : JSON.stringify(req.body);
      event = stripeClient.webhooks.constructEvent(rawBody, sig, WH_SECRET);
    } else {
      // No webhook secret — parse event directly (for initial testing)
      event = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
    }

    console.log('Webhook event:', event.type);

    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object;
        const customerEmail = session.customer_details?.email || session.customer_email;
        const customerId = session.customer;
        const subscriptionId = session.subscription;
        const plan = session.metadata?.plan || 'premium';
        const hiveUid = session.metadata?.hive_uid;

        console.log(`Checkout completed: email=${customerEmail}, customer=${customerId}, plan=${plan}, uid=${hiveUid}`);

        // Tell Hive API to activate premium for this account
        const resp = await fetch(`${HIVE_API}?action=set-premium&admin_key=${encodeURIComponent(ADMIN_KEY)}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            admin_key: ADMIN_KEY,
            email: customerEmail,
            plan,
            customerId,
            subscriptionId,
            hiveUid
          }),
          signal: AbortSignal.timeout(10000)
        });

        const result = await resp.json();
        if (!resp.ok) {
          console.error('set-premium failed:', result);
        } else {
          console.log('set-premium success:', result.message);
        }
        break;
      }

      case 'customer.subscription.deleted': {
        const sub = event.data.object;
        const customerId = sub.customer;

        console.log(`Subscription deleted: customer=${customerId}`);

        const resp = await fetch(`${HIVE_API}?action=cancel-premium&admin_key=${encodeURIComponent(ADMIN_KEY)}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            admin_key: ADMIN_KEY,
            customerId
          }),
          signal: AbortSignal.timeout(10000)
        });

        if (!resp.ok) {
          const result = await resp.json();
          console.error('cancel-premium failed:', result);
        }
        break;
      }

      case 'invoice.payment_failed': {
        const invoice = event.data.object;
        const customerId = invoice.customer;
        console.log(`Payment failed: customer=${customerId}`);
        // Could send notification here in the future
        break;
      }

      default:
        console.log(`Unhandled event: ${event.type}`);
    }

    return res.json({ received: true });
  } catch (err) {
    console.error('Webhook error:', err);
    return res.status(400).json({ error: 'Webhook error' });
  }
}
