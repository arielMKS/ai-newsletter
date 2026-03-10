# 🤖 AI Morning Brief — Setup Guide

A daily newsletter that emails you the top AI news every morning at 9 AM,
with each article summarised by Claude.

---

## What you'll need (all free)

| Thing | Where to get it |
|---|---|
| **Anthropic API key** | platform.anthropic.com → API Keys |
| **Gmail App Password** | See Step 2 below |
| **Railway account** | railway.app (free tier) |
| **GitHub account** | github.com (free) |

---

## Step 1 — Get your Anthropic API key

1. Go to **platform.anthropic.com** and sign in.
2. Click **API Keys** → **Create Key**.
3. Copy it — you'll paste it into Railway later.

> New accounts get $5 free credit. Each daily newsletter costs roughly $0.01–0.02.

---

## Step 2 — Create a Gmail App Password

Google requires an "App Password" instead of your real password for SMTP.

1. Go to **myaccount.google.com/security**
2. Make sure **2-Step Verification** is ON (required)
3. Search for **"App Passwords"** in the search bar
4. Choose app: **Mail**, device: **Other** → type "Newsletter Bot"
5. Click **Generate** → copy the 16-character password (e.g. `abcd efgh ijkl mnop`)

---

## Step 3 — Push code to GitHub

1. Create a new **private** GitHub repo (e.g. `ai-newsletter`)
2. Upload these four files into it:
   - `newsletter.py`
   - `requirements.txt`
   - `Dockerfile`
   - `railway.json`

---

## Step 4 — Deploy to Railway

1. Go to **railway.app** → **New Project** → **Deploy from GitHub repo**
2. Select your `ai-newsletter` repo
3. Once imported, click **Variables** and add these five:

| Variable | Value |
|---|---|
| `ANTHROPIC_API_KEY` | your Anthropic key |
| `GMAIL_ADDRESS` | you@gmail.com |
| `GMAIL_APP_PASSWORD` | the 16-char app password |
| `RECIPIENT_EMAIL` | who gets the email (can be same as above) |
| `NUM_ARTICLES` | `8` (or `5` or `10`) |

4. Railway reads `railway.json` automatically — the cron `"0 9 * * *"` means **9:00 AM UTC**.

> **Timezone note:** If you're in a different timezone, adjust the hour:
> - US Eastern (EST): use `0 14 * * *` (9 AM EST = 2 PM UTC)
> - US Pacific (PST): use `0 17 * * *`
> - UK (GMT): use `0 9 * * *` ✓

---

## Step 5 — Test it immediately

In Railway, go to your service → **Settings** → **Trigger Run** to fire it right now
and confirm the email arrives before waiting until morning.

---

## Customising news topics

To focus on a specific AI sub-topic, edit the Google News RSS URL in `newsletter.py`:

```python
# Current (general AI):
"https://news.google.com/rss/search?q=artificial+intelligence+AI&hl=en-US&gl=US&ceid=US:en"

# Examples:
# LLMs only:   q=large+language+models+LLM
# AI safety:   q=AI+safety+alignment
# AI + business: q=AI+enterprise+business
```

---

## Costs

- **Railway**: Free tier includes 500 hours/month — a daily cron job uses ~1 minute/day, well within limits.
- **Anthropic API**: ~$0.01–0.02 per run (8 article summaries with claude-sonnet).
- **Gmail SMTP**: Free.

Total: essentially **free**.
