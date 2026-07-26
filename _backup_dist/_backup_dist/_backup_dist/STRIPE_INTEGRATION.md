# Stripe Payment Integration — The Signal

## Overview

Stripe payment integration for Signal Premium ($9/mo) and Pro ($29/mo) subscriptions.

## Required Environment Variables

Set these in Vercel project settings (https://vercel.com/beachsquadlas-projects/the-signal/settings/environment-variables):

| Variable | Description | Example |
|---|---|---|
| `STRIPE_SECRET_KEY` | Your Stripe secret key (starts with `sk_live_` or `sk_test_`) | `sk_live_abc123...` |
| `STRIPE_PREMIUM_PRICE_ID` | Stripe Price ID for Premium ($9/mo) plan | `price_premium_abc123` |
| `STRIPE_PRO_PRICE_ID` | Stripe Price ID for Pro ($29/mo) plan | `price_pro_abc123` |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret (for `whsec_...`) | `whsec_abc123...` |
| `ADMIN_KEY` | Admin key for webhook-to-Hive-API communication | `signal_admin_2026` |

## How to set up Stripe prices

1. Go to https://dashboard.stripe.com/products
2. Create two products:
   - **Premium** — $9/month (recurring)
   - **Pro** — $29/month (recurring)
3. Copy the Price IDs (starts with `price_...`)
4. Set them as `STRIPE_PREMIUM_PRICE_ID` and `STRIPE_PRO_PRICE_ID` in Vercel env vars

## How to set up the webhook

1. Go to https://dashboard.stripe.com/webhooks
2. Add endpoint: `https://readthesignal.net/api/stripe-webhook`
3. Listen for events:
   - `checkout.session.completed`
   - `customer.subscription.deleted`
   - `invoice.payment_failed`
4. Copy the signing secret (`whsec_...`) and set as `STRIPE_WEBHOOK_SECRET`

## Files created/modified

### Pricing page
- `pricing/index.html` → Source file for `/pricing` page
- `_backup_dist/pricing/index.html` → Backup copy

### API endpoints
- `api/create-checkout.mjs` → Creates Stripe Checkout Sessions (POST)
- `api/activate-premium.mjs` → Verifies session & activates premium (POST)
- `api/stripe-webhook.mjs` → Handles post-payment events (webhook)

### Success page
- `_backup_dist/premium/success.html` → Post-checkout success page at `/premium/success`

### Config
- `vercel.json` → Routes for `/premium` and `/premium/success`

## Checkout flow

1. User clicks "Subscribe Now" on `/pricing`
2. Frontend calls `POST /api/create-checkout` with `{ plan, token }`
3. Server resolves Hive user, creates Stripe Checkout Session
4. User redirected to Stripe Checkout for payment
5. On success → redirected to `/premium/success?session_id=...`
6. Success page calls `POST /api/activate-premium` to verify + activate
7. Webhook also activates premium as backup (via `stripe-webhook.mjs`)
8. User sees "Welcome to Premium!" and is redirected to `/premium`
