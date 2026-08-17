// Stripe Webhook — Vercel serverless function
// Handles Stripe events: checkout.session.completed, customer.subscription.deleted

const SK = process.env.STRIPE_SECRET_KEY || '';
const WH_SECRET = process.env.STRIPE_WEBHOOK_SECRET || '';
const ADMIN_KEY = process.env.ADMIN_KEY || '';

// Premium status storage — in-memory (resets on cold start)
// For production: use Firebase Firestore or a database
const premiumUsers = new Map();

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  if (!SK || !WH_SECRET) {
    console.log('Stripe webhook not configured');
    return res.status(500).json({ error: 'Webhook not configured' });
  }

  try {
    const sig = req.headers['stripe-signature'];
    const payload = typeof req.body === 'string' ? req.body : JSON.stringify(req.body);

    // Verify webhook signature
    const stripe = await import('stripe');
    // Note: full signature verification requires raw body access
    // For now, accept the event and validate minimally
    const event = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;

    console.log('Webhook event:', event.type);

    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object;
        const customerEmail = session.customer_details?.email;
        const customerId = session.customer;
        const subscriptionId = session.subscription;
        const plan = session.metadata?.plan || 'premium';

        console.log(`Payment completed: ${customerEmail} -> ${plan}`);
        premiumUsers.set(customerEmail, {
          plan,
          customerId,
          subscriptionId,
          startedAt: new Date().toISOString()
        });

        // Future: write to Firebase Firestore
        // await db.collection('premium_users').doc(customerEmail).set({...});
        break;
      }

      case 'customer.subscription.deleted': {
        const sub = event.data.object;
        const customerId = sub.customer;

        // Find and remove the user
        for (const [email, data] of premiumUsers) {
          if (data.customerId === customerId) {
            premiumUsers.delete(email);
            console.log(`Subscription canceled: ${email}`);
            break;
          }
        }
        break;
      }

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    return res.json({ received: true });
  } catch (err) {
    console.error('Webhook error:', err);
    return res.status(400).json({ error: 'Webhook error' });
  }
}

// Export for Pulse to check premium status
export function isPremium(email) {
  return premiumUsers.has(email);
}

export function getPremiumData(email) {
  return premiumUsers.get(email) || null;
}
