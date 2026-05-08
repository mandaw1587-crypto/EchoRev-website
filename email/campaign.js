#!/usr/bin/env node
/**
 * EchoRev AI Syndicate — Local Business Email Campaign
 *
 * Usage:
 *   node campaign.js outreach     # send initial outreach emails
 *   node campaign.js followup     # send follow-ups to non-responders
 *   node campaign.js preview <n>  # preview email #n without sending
 *   node campaign.js stats        # show campaign stats
 */

require('dotenv').config();
const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');
const { parse, stringify } = require('csv-parse/sync') && require('./csvHelper');

// ── Config ────────────────────────────────────────────────────────
const CONFIG = {
  smtpHost: process.env.SMTP_HOST || 'smtp.gmail.com',
  smtpPort: parseInt(process.env.SMTP_PORT || '587'),
  smtpSecure: process.env.SMTP_SECURE === 'true',
  smtpUser: process.env.SMTP_USER,
  smtpPass: process.env.SMTP_PASS,
  fromAddress: process.env.FROM_ADDRESS,
  senderName: process.env.SENDER_NAME || 'EchoRev Team',
  senderTitle: process.env.SENDER_TITLE || 'Founder, EchoRev AI Syndicate',
  senderEmail: process.env.SENDER_EMAIL,
  bookingLink: process.env.BOOKING_LINK || 'https://calendly.com/echorev',
  websiteUrl: process.env.WEBSITE_URL || 'https://echorev.com',
  unsubscribeUrl: process.env.UNSUBSCRIBE_URL || 'https://echorev.com/unsubscribe',
  delayMs: parseInt(process.env.EMAIL_DELAY_MS || '5000'),
  followupDelayDays: parseInt(process.env.FOLLOWUP_DELAY_DAYS || '4'),
  maxPerRun: parseInt(process.env.MAX_EMAILS_PER_RUN || '50'),
};

const CONTACTS_FILE = path.join(__dirname, 'contacts.csv');
const TEMPLATE_DIR = path.join(__dirname, 'templates');

// ── Helpers ───────────────────────────────────────────────────────

function loadContacts() {
  const raw = fs.readFileSync(CONTACTS_FILE, 'utf8');
  const lines = raw.trim().split('\n');
  const headers = lines[0].split(',');
  return lines.slice(1).map(line => {
    const vals = line.split(',');
    return headers.reduce((obj, h, i) => {
      obj[h.trim()] = (vals[i] || '').trim();
      return obj;
    }, {});
  });
}

function saveContacts(contacts) {
  const headers = Object.keys(contacts[0]);
  const rows = [headers.join(',')];
  contacts.forEach(c => {
    rows.push(headers.map(h => c[h] || '').join(','));
  });
  fs.writeFileSync(CONTACTS_FILE, rows.join('\n') + '\n', 'utf8');
}

function loadTemplate(name) {
  return fs.readFileSync(path.join(TEMPLATE_DIR, `${name}.html`), 'utf8');
}

function renderTemplate(template, contact) {
  return template
    .replace(/{{OWNER_NAME}}/g, contact.owner_name)
    .replace(/{{BUSINESS_NAME}}/g, contact.business_name)
    .replace(/{{BUSINESS_TYPE}}/g, contact.business_type)
    .replace(/{{CITY}}/g, contact.city)
    .replace(/{{SENDER_NAME}}/g, CONFIG.senderName)
    .replace(/{{SENDER_TITLE}}/g, CONFIG.senderTitle)
    .replace(/{{SENDER_EMAIL}}/g, CONFIG.senderEmail)
    .replace(/{{BOOKING_LINK}}/g, CONFIG.bookingLink)
    .replace(/{{WEBSITE_URL}}/g, CONFIG.websiteUrl)
    .replace(/{{UNSUBSCRIBE_LINK}}/g, `${CONFIG.unsubscribeUrl}?email=${encodeURIComponent(contact.email)}`);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function daysSince(dateStr) {
  if (!dateStr) return Infinity;
  return (Date.now() - new Date(dateStr).getTime()) / (1000 * 60 * 60 * 24);
}

function createTransport() {
  return nodemailer.createTransport({
    host: CONFIG.smtpHost,
    port: CONFIG.smtpPort,
    secure: CONFIG.smtpSecure,
    auth: { user: CONFIG.smtpUser, pass: CONFIG.smtpPass },
  });
}

// ── Commands ──────────────────────────────────────────────────────

async function sendOutreach() {
  const contacts = loadContacts();
  const transport = createTransport();
  const template = loadTemplate('outreach');

  const queue = contacts.filter(c =>
    c.unsubscribed !== 'true' &&
    c.sent !== 'true'
  ).slice(0, CONFIG.maxPerRun);

  if (queue.length === 0) {
    console.log('No unsent contacts remaining.');
    return;
  }

  console.log(`Sending outreach to ${queue.length} contacts...\n`);

  for (const contact of queue) {
    const html = renderTemplate(template, contact);
    const subject = `AI for ${contact.business_name} — Free 30-min Strategy Call`;

    try {
      await transport.sendMail({
        from: CONFIG.fromAddress,
        to: contact.email,
        subject,
        html,
      });

      contact.sent = 'true';
      contact.sent_date = new Date().toISOString().split('T')[0];
      console.log(`✅  Sent → ${contact.business_name} (${contact.email})`);
    } catch (err) {
      console.error(`❌  Failed → ${contact.email}: ${err.message}`);
    }

    saveContacts(contacts);
    await sleep(CONFIG.delayMs);
  }

  console.log('\nOutreach run complete.');
}

async function sendFollowups() {
  const contacts = loadContacts();
  const transport = createTransport();
  const template = loadTemplate('followup');

  const queue = contacts.filter(c =>
    c.unsubscribed !== 'true' &&
    c.sent === 'true' &&
    c.replied !== 'true' &&
    c.followup_sent !== 'true' &&
    daysSince(c.sent_date) >= CONFIG.followupDelayDays
  ).slice(0, CONFIG.maxPerRun);

  if (queue.length === 0) {
    console.log('No follow-ups ready to send.');
    return;
  }

  console.log(`Sending follow-ups to ${queue.length} contacts...\n`);

  for (const contact of queue) {
    const html = renderTemplate(template, contact);
    const subject = `Re: AI for ${contact.business_name} — quick follow-up`;

    try {
      await transport.sendMail({
        from: CONFIG.fromAddress,
        to: contact.email,
        subject,
        html,
      });

      contact.followup_sent = 'true';
      contact.followup_date = new Date().toISOString().split('T')[0];
      console.log(`✅  Follow-up → ${contact.business_name} (${contact.email})`);
    } catch (err) {
      console.error(`❌  Failed → ${contact.email}: ${err.message}`);
    }

    saveContacts(contacts);
    await sleep(CONFIG.delayMs);
  }

  console.log('\nFollow-up run complete.');
}

function previewEmail(indexStr) {
  const index = parseInt(indexStr || '0');
  const contacts = loadContacts();
  const contact = contacts[index];
  if (!contact) {
    console.error(`No contact at index ${index}`);
    process.exit(1);
  }

  const template = loadTemplate('outreach');
  const html = renderTemplate(template, contact);

  const previewPath = path.join(__dirname, 'preview.html');
  fs.writeFileSync(previewPath, html, 'utf8');
  console.log(`Preview written to: ${previewPath}`);
  console.log(`Contact: ${contact.owner_name} — ${contact.business_name}`);
}

function showStats() {
  const contacts = loadContacts();
  const total = contacts.length;
  const sent = contacts.filter(c => c.sent === 'true').length;
  const followedUp = contacts.filter(c => c.followup_sent === 'true').length;
  const replied = contacts.filter(c => c.replied === 'true').length;
  const unsubscribed = contacts.filter(c => c.unsubscribed === 'true').length;

  console.log('\n📊  EchoRev Campaign Stats');
  console.log('─'.repeat(36));
  console.log(`  Total contacts:    ${total}`);
  console.log(`  Outreach sent:     ${sent}`);
  console.log(`  Follow-ups sent:   ${followedUp}`);
  console.log(`  Replies:           ${replied}  (${total > 0 ? ((replied/sent||0)*100).toFixed(1) : 0}% reply rate)`);
  console.log(`  Unsubscribed:      ${unsubscribed}`);
  console.log(`  Pending outreach:  ${total - sent - unsubscribed}`);
  console.log('─'.repeat(36) + '\n');
}

// ── Entry Point ───────────────────────────────────────────────────

const [,, command, arg] = process.argv;

switch (command) {
  case 'outreach':  sendOutreach(); break;
  case 'followup':  sendFollowups(); break;
  case 'preview':   previewEmail(arg); break;
  case 'stats':     showStats(); break;
  default:
    console.log(`
EchoRev Email Campaign

Usage:
  node campaign.js outreach      Send initial outreach emails
  node campaign.js followup      Send follow-ups (${CONFIG.followupDelayDays}+ days after outreach)
  node campaign.js preview [n]   Preview email for contact #n (default: 0)
  node campaign.js stats         Show campaign statistics
    `);
}
