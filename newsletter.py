import os
import smtplib
import feedparser
import anthropic
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from bs4 import BeautifulSoup

# ── Config (set these as environment variables) ──────────────────────────────
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GMAIL_ADDRESS     = os.environ["GMAIL_ADDRESS"]       # your Gmail address
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"] # Gmail App Password (not your login password)
RECIPIENT_EMAIL   = os.environ.get("RECIPIENT_EMAIL", GMAIL_ADDRESS)
NUM_ARTICLES      = int(os.environ.get("NUM_ARTICLES", "8"))

# ── RSS feeds for AI news ────────────────────────────────────────────────────
RSS_FEEDS = [
    "https://news.google.com/rss/search?q=artificial+intelligence+AI&hl=en-US&gl=US&ceid=US:en",
    "https://feeds.feedburner.com/venturebeat/SZYF",  # VentureBeat AI
    "https://www.technologyreview.com/feed/",          # MIT Tech Review
]

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def fetch_articles(num: int) -> list[dict]:
    """Fetch and deduplicate articles from RSS feeds."""
    seen, articles = set(), []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link  = entry.get("link", "").strip()
            if not title or not link or title in seen:
                continue
            seen.add(title)
            # Try to grab a short snippet from the entry summary
            raw_summary = entry.get("summary", "") or entry.get("description", "")
            snippet = BeautifulSoup(raw_summary, "html.parser").get_text()[:400]
            articles.append({"title": title, "link": link, "snippet": snippet})
            if len(articles) >= num * 2:   # collect extra, Claude will pick best
                break
        if len(articles) >= num * 2:
            break
    return articles[:num * 2]


def summarize_articles(articles: list[dict], keep: int) -> list[dict]:
    """Use Claude to pick the most newsworthy articles and summarize each."""
    article_text = "\n\n".join(
        f"[{i+1}] TITLE: {a['title']}\nSNIPPET: {a['snippet']}\nURL: {a['link']}"
        for i, a in enumerate(articles)
    )

    prompt = f"""You are an AI news editor. Below are {len(articles)} recent AI articles.

Your job:
1. Select the {keep} most important / newsworthy articles covering a variety of topics.
2. For each selected article write a 2-3 sentence summary in plain English — clear, insightful, no hype.
3. Return ONLY a JSON array (no markdown fences) with objects like:
   {{"rank": 1, "title": "...", "url": "...", "summary": "..."}}

ARTICLES:
{article_text}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    import json, re
    raw = response.content[0].text
    # Strip any accidental markdown fences
    raw = re.sub(r"```(?:json)?|```", "", raw).strip()
    return json.loads(raw)


def build_html(summaries: list[dict]) -> str:
    today = datetime.now().strftime("%A, %B %d, %Y")
    cards = ""
    for item in summaries:
        cards += f"""
        <div style="background:#ffffff;border-radius:12px;padding:24px 28px;
                    margin-bottom:20px;box-shadow:0 1px 4px rgba(0,0,0,.08);
                    border-left:4px solid #6c63ff;">
          <a href="{item['url']}" style="font-size:17px;font-weight:700;
             color:#1a1a2e;text-decoration:none;line-height:1.4;">
            {item['title']}
          </a>
          <p style="margin:10px 0 14px;color:#444;font-size:14px;line-height:1.6;">
            {item['summary']}
          </p>
          <a href="{item['url']}" style="font-size:13px;color:#6c63ff;
             font-weight:600;text-decoration:none;">Read full article →</a>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f4f4f8;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr><td align="center" style="padding:40px 16px;">
      <table width="620" cellpadding="0" cellspacing="0" style="max-width:620px;width:100%;">

        <!-- Header -->
        <tr><td style="background:linear-gradient(135deg,#6c63ff,#3ecfcf);
                       border-radius:14px 14px 0 0;padding:36px 32px;text-align:center;">
          <div style="font-size:28px;font-weight:800;color:#fff;letter-spacing:-0.5px;">
            🤖 AI Morning Brief
          </div>
          <div style="color:rgba(255,255,255,.85);font-size:14px;margin-top:6px;">
            {today}
          </div>
        </td></tr>

        <!-- Intro -->
        <tr><td style="background:#fff;padding:24px 32px 8px;">
          <p style="margin:0;color:#555;font-size:15px;line-height:1.6;">
            Good morning! Here are today's top {len(summaries)} developments in AI — 
            curated and summarised just for you.
          </p>
        </td></tr>

        <!-- Articles -->
        <tr><td style="background:#f4f4f8;padding:20px 28px 8px;">
          {cards}
        </td></tr>

        <!-- Footer -->
        <tr><td style="background:#fff;border-radius:0 0 14px 14px;
                       padding:20px 32px;text-align:center;
                       border-top:1px solid #eee;">
          <p style="margin:0;color:#aaa;font-size:12px;">
            Delivered by your AI Newsletter Bot • Powered by Claude &amp; Google News
          </p>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


def send_email(html: str, subject: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_ADDRESS
    msg["To"]      = RECIPIENT_EMAIL
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
    print(f"✅ Newsletter sent to {RECIPIENT_EMAIL}")


def main():
    print("📰 Fetching AI news articles…")
    articles = fetch_articles(NUM_ARTICLES)
    print(f"   Found {len(articles)} articles. Summarising with Claude…")
    summaries = summarize_articles(articles, NUM_ARTICLES)
    print(f"   Got {len(summaries)} summaries. Building email…")
    html = build_html(summaries)
    today_str = datetime.now().strftime("%b %d")
    send_email(html, subject=f"🤖 AI Morning Brief — {today_str}")


if __name__ == "__main__":
    main()
