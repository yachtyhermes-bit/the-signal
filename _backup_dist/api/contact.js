// api/contact.js — Contact form handler for The Signal
// Sends messages from the About page contact form to Beachsquadla@gmail.com
//
// ENV VARS REQUIRED (set in Vercel):
//   GMAIL_APP_PASSWORD — Gmail app password for Beachsquadla@gmail.com
//   CONTACT_TO_EMAIL  — Beachsquadla@gmail.com
//
// How to get a Gmail app password:
//   1. Enable 2FA on your Google account (if not already)
//   2. Go to https://myaccount.google.com/apppasswords
//   3. Create app named "The Signal Contact Form"
//   4. Copy the 16-char password and set it as GMAIL_APP_PASSWORD in Vercel

const nodemailer = require('nodemailer');

const TO_EMAIL = process.env.CONTACT_TO_EMAIL || 'ReadtheSignalSupport@gmail.com';
const FROM_EMAIL = process.env.CONTACT_FROM_EMAIL || 'ReadtheSignalSupport@gmail.com';
const APP_PASSWORD = process.env.GMAIL_APP_PASSWORD;

function createTransporter() {
  if (!APP_PASSWORD) {
    return null;
  }
  return nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: FROM_EMAIL,
      pass: APP_PASSWORD,
    },
  });
}

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { name, email, message } = req.body || {};

  // Validate
  if (!name || !name.trim()) {
    return res.status(400).json({ error: 'Name is required' });
  }
  if (!email || !email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: 'A valid email address is required' });
  }
  if (!message || !message.trim() || message.trim().length < 10) {
    return res.status(400).json({ error: 'Message must be at least 10 characters' });
  }

  // Check if email sending is configured
  const transporter = createTransporter();
  if (!transporter) {
    // Save message to local file as fallback (Vercel can't write)
    console.log('CONTACT FORM SUBMISSION (GMAIL_APP_PASSWORD not set):');
    console.log(`  From: ${name} <${email}>`);
    console.log(`  Message: ${message}`);
    return res.status(200).json({
      success: true,
      message: 'Message received! We\'ll get back to you soon.',
      note: 'GMAIL_APP_PASSWORD not configured. Message logged to console.'
    });
  }

  try {
    await transporter.sendMail({
      from: `"The Signal Contact" <${FROM_EMAIL}>`,
      to: TO_EMAIL,
      replyTo: email,
      subject: `[The Signal Contact] ${name} — ${email}`,
      text: `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`,
      html: `
        <h2>New Contact Form Submission</h2>
        <table style="border-collapse:collapse;width:100%;max-width:500px">
          <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold">Name</td><td style="padding:8px;border:1px solid #ddd">${name}</td></tr>
          <tr><td style="padding:8px;border:1px solid #ddd;font-weight:bold">Email</td><td style="padding:8px;border:1px solid #ddd"><a href="mailto:${email}">${email}</a></td></tr>
        </table>
        <h3>Message</h3>
        <p style="background:#f5f5f5;padding:12px;border-radius:6px;white-space:pre-wrap">${message}</p>
        <hr>
        <p style="color:#888;font-size:12px">Sent from readthesignal.net contact form</p>
      `,
    });

    return res.status(200).json({
      success: true,
      message: 'Message sent! We\'ll get back to you soon.'
    });
  } catch (err) {
    console.error('Contact form email failed:', err);
    return res.status(500).json({
      error: 'Failed to send message. Please try again later.',
      details: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
  }
};
