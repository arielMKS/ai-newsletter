# 🤖 AI Morning Brief — Setup Guide

A daily newsletter that emails you the top AI news every morning at 9 AM,
with each article summarised by Claude. Runs entirely on GitHub — no extra
accounts or servers needed.

---

## What you'll need (all free)

| Thing | Where to get it |
|---|---|
| **Anthropic API key** | platform.anthropic.com → API Keys |
| **Gmail App Password** | See Step 2 below |
| **GitHub account** | github.com (free) |

---

## Step 1 — Get your Anthropic API key

1. Go to **platform.anthropic.com** and sign in.
2. Click **API Keys** → **Create Key**.
3. Copy it — you'll paste it into GitHub later.

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

## Step 3 — Create a GitHub repo and upload files

1. Go to **github.com** → **New repository**
2. Name it `ai-newsletter`, set it to **Private**, click **Create**
3. Upload these two files into the root of the repo:
   - `newsletter.py`
   - `requirements.txt`
4. Then create the workflow file by clicking **Add file → Create new file**,
   type `.github/workflows/newsletter.yml` in the filename box (GitHub creates
   the folders automatically), paste the contents of `newsletter.yml`, and commit.

---

## Step 4 — Add your secrets to GitHub

GitHub Actions uses encrypted "Secrets" so your passwords never appear in code.

1. In your repo go to **Settings → Secrets and variables → Actions**
2. Click **New repository secret** and add each of these:

| Secret name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | your Anthropic key |
| `GMAIL_ADDRESS` | you@gmail.com |
| `GMAIL_APP_PASSWORD` | the 16-char app password |
| `RECIPIENT_EMAIL` | who gets the email (can be same Gmail) |

---

## Step 5 — Adjust your timezone

Open `newsletter.yml` and find this line:

```yaml
- cron: "0 14 * * *"   # 9 AM EST
```

Change the hour to match your timezone (the schedule runs in UTC):

| Your timezone | Cron for 9 AM |
|---|---|
| US Eastern (EST) | `0 14 * * *` |
| US Central (CST) | `0 15 * * *` |
| US Mountain (MST) | `0 16 * * *` |
| US Pacific (PST) | `0 17 * * *` |
| UK (GMT) | `0 9 * * *` |
| Central Europe (CET) | `0 8 * * *` |

---

## Step 6 — Test it immediately

1. In your repo, click the **Actions** tab
2. Click **AI Morning Brief** in the left sidebar
3. Click **Run workflow** → **Run workflow**
4. Within ~30 seconds your email should arrive!

---

## Customising news topics

Edit the Google News RSS URL in `newsletter.py`:

```python
# Current (general AI):
"https://news.google.com/rss/search?q=artificial+intelligence+AI&hl=en-US&gl=US&ceid=US:en"

# Examples:
# LLMs only:      q=large+language+models+LLM
# AI safety:      q=AI+safety+alignment
# AI + business:  q=AI+enterprise+business
```

---

## Costs

- **GitHub Actions**: Free tier = 2,000 min/month. Each run ≈ 1 min → ~30/month, well within limits.
- **Anthropic API**: ~$0.01–0.02 per run.
- **Gmail SMTP**: Free.

Total: essentially **free**.
